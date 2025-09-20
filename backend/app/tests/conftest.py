"""Pytest fixtures."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.main import app  # noqa: E402
from app.core.redis import redis_client  # noqa: E402
from app.db.session import Base  # noqa: E402
from app.api.deps import get_db  # noqa: E402

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine  # noqa: E402

test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


class DummyRedis:
    def __init__(self) -> None:
        self.storage: dict[str, str] = {}

    async def get(self, key: str):
        return self.storage.get(key)

    async def set(self, key: str, value: str, ex: int | None = None):
        self.storage[key] = value

    async def lrange(self, key: str, start: int, end: int):
        return []

    async def lpush(self, key: str, value: str):
        self.storage.setdefault(key, [])
        self.storage[key].insert(0, value)

    async def ltrim(self, key: str, start: int, end: int):
        if key in self.storage:
            self.storage[key] = self.storage[key][start : end + 1]

    async def incr(self, key: str):
        self.storage[key] = str(int(self.storage.get(key, "0")) + 1)
        return int(self.storage[key])

    async def expire(self, key: str, ttl: int):
        return True

    async def close(self):
        return True


@pytest_asyncio.fixture(autouse=True)
async def mock_redis(monkeypatch):
    client = DummyRedis()

    async def connect():
        redis_client._redis = client  # type: ignore[attr-defined]

    async def disconnect():
        redis_client._redis = None  # type: ignore[attr-defined]

    monkeypatch.setattr(redis_client, "connect", connect)
    monkeypatch.setattr(redis_client, "disconnect", disconnect)
    redis_client._redis = client  # type: ignore[attr-defined]
    yield
    redis_client._redis = None  # type: ignore[attr-defined]


@pytest_asyncio.fixture(autouse=True)
async def override_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.pop(get_db, None)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def client(mock_redis) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
