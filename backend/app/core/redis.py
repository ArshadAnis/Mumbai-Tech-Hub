"""Async Redis client wrapper for reuse across modules."""
from __future__ import annotations

import json
import logging
from typing import Any

from redis.asyncio import Redis, from_url

from app.core.config import settings


logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self) -> None:
        self._redis: Redis | None = None

    @property
    def client(self) -> Redis:
        if not self._redis:
            raise RuntimeError("Redis client not connected")
        return self._redis

    async def connect(self) -> None:
        if self._redis:
            return
        logger.info("Connecting to Redis at %s", settings.redis_url)
        self._redis = await from_url(str(settings.redis_url), decode_responses=True)

    async def disconnect(self) -> None:
        if self._redis:
            await self._redis.close()
            self._redis = None

    async def get_json(self, key: str) -> Any:
        data = await self.client.get(key)
        if data:
            return json.loads(data)
        return None

    async def set_json(self, key: str, value: Any, expire: int | None = None) -> None:
        await self.client.set(key, json.dumps(value), ex=expire)


redis_client = RedisClient()
