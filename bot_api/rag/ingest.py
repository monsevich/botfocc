"""Document ingestion utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

import asyncio

from docx import Document

from ..db import pg
from .yandex_fm import YandexFoundationModel
from qdrant_client import AsyncQdrantClient, models

CHUNK_MIN = 800
CHUNK_MAX = 1500


def _chunk_text(text: str) -> List[str]:
    chunks, buf = [], ""
    for paragraph in text.splitlines():
        if len(buf) + len(paragraph) > CHUNK_MAX:
            if len(buf) >= CHUNK_MIN:
                chunks.append(buf)
            buf = paragraph
        else:
            buf += "\n" + paragraph
    if buf:
        chunks.append(buf)
    return chunks


def _load_file(path: Path) -> str:
    if path.suffix == ".docx":
        return "\n".join(p.text for p in Document(path).paragraphs)
    if path.suffix == ".md":
        return path.read_text(encoding="utf-8")
    return ""


async def reindex_kb() -> None:
    """Rebuild knowledge base vectors from stored files."""
    settings = pg.settings  # assumes settings assigned externally
    yfm = YandexFoundationModel(settings.yfm_api_key, settings.yfm_folder_id)
    qdrant = AsyncQdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    path = Path(settings.kb_path)
    texts: List[str] = []
    for file in path.glob("**/*"):
        if file.suffix in {".docx", ".md"}:
            texts.append(_load_file(file))
    chunks = [c for t in texts for c in _chunk_text(t)]
    vectors = await yfm.embed(chunks)
    pool = await pg.get_pool(settings.database_dsn)
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM kb_chunks")
        for idx, (chunk, vector) in enumerate(zip(chunks, vectors)):
            await conn.execute(
                "INSERT INTO kb_chunks(id, content) VALUES ($1, $2)", idx, chunk
            )
            await qdrant.upsert(
                collection_name="kb",
                points=[models.PointStruct(id=idx, vector=vector, payload={"text": chunk})],
            )
