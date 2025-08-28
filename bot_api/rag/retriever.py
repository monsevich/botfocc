"""Vector retrieval from Qdrant."""
from typing import List, Tuple

from qdrant_client import AsyncQdrantClient, models

from .yandex_fm import YandexFoundationModel


async def retrieve(
    query: str,
    yfm: YandexFoundationModel,
    qdrant: AsyncQdrantClient,
    top_k: int = 5,
    filters: dict | None = None,
) -> List[Tuple[str, float]]:
    """Return top-k matching chunks and their scores."""
    vector = (await yfm.embed([query]))[0]
    result = await qdrant.search(
        collection_name="kb",
        query_vector=vector,
        limit=top_k,
        query_filter=models.Filter.from_dict(filters or {}),
    )
    return [(r.payload.get("text", ""), r.score) for r in result]
