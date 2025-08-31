from __future__ import annotations

import redis.asyncio as aioredis

from .config import settings

_redis: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


async def set_idempotency_key(key: str, ttl_seconds: int = 24 * 3600) -> bool:
    r = await get_redis()
    # SET NX EX гарантирует, что «победит» только первый запрос
    return await r.set(f"idempotency:{key}", "1", nx=True, ex=ttl_seconds) is True
