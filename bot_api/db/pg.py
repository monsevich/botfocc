"""Asyncpg helpers."""
from __future__ import annotations

from typing import Any, Iterable

import asyncpg

from ..settings import Settings

settings: Settings  # to be set by caller
_pool: asyncpg.Pool | None = None


async def get_pool(dsn: str) -> asyncpg.Pool:
    """Return shared connection pool."""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(dsn)
    return _pool


async def fetch(query: str, *args: Any) -> list[asyncpg.Record]:
    pool = await get_pool(settings.database_dsn)
    async with pool.acquire() as conn:
        return await conn.fetch(query, *args)


async def execute(query: str, *args: Any) -> str:
    pool = await get_pool(settings.database_dsn)
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)
