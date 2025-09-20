"""Simple token bucket rate limiter backed by Redis."""
from __future__ import annotations

import time

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.redis import redis_client


async def rate_limit(key: str, limit: int | None = None, window: int | None = None) -> None:
    limit = limit or settings.rate_limit_default
    window = window or settings.rate_limit_window_seconds
    redis = redis_client.client
    now = int(time.time())
    bucket_key = f"ratelimit:{key}:{now // window}"
    current = await redis.incr(bucket_key)
    if current == 1:
        await redis.expire(bucket_key, window)
    if current > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please slow down.",
        )
