"""Document ingestion utilities."""
from qdrant_client import AsyncQdrantClient, models
from ..db import pg
from .yandex_fm import YandexFoundationModel

COLLECTION = "kb"

async def reindex_kb() -> None:
    settings = pg.settings
    yfm = YandexFoundationModel(settings.yfm_api_key, settings.yfm_folder_id)
    qdrant = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)

    # 1) Забираем опубликованные чанки из Django-БД
    rows = await pg.fetch(
        """
        SELECT kc.id, kc.text
        FROM kb_chunk kc
        JOIN kb_entry ke ON kc.entry_id = ke.id
        WHERE ke.is_published = TRUE
        ORDER BY kc.id
        """
    )
    texts = [r["text"] for r in rows]
    ids = [int(r["id"]) for r in rows]
    if not texts:
        return

    # 2) Эмбеддинги
    vectors = await yfm.embed(texts)
    dim = len(vectors[0])

    # 3) Гарантируем коллекцию
    await qdrant.recreate_collection(
        collection_name=COLLECTION,
        vectors_config=models.VectorParams(size=dim, distance=models.Distance.COSINE),
    )

    # 4) Апсерты
    points = [
        models.PointStruct(id=ids[i], vector=vectors[i], payload={"text": texts[i]})
        for i in range(len(ids))
    ]
    await qdrant.upsert(collection_name=COLLECTION, points=points)
