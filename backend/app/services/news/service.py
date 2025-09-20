"""Mock news provider with caching."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from app.core.redis import redis_client

CACHE_KEY = "news:latest"
CACHE_TTL = 60


async def fetch_news() -> List[dict[str, str]]:
    cached = await redis_client.get_json(CACHE_KEY)
    if cached:
        return cached
    news = [
        {
            "title": "Crypto markets steady",
            "summary": "BTC consolidates near key levels.",
            "published_at": datetime.utcnow().isoformat(),
            "disclaimer": "Not financial advice.",
        }
    ]
    await redis_client.set_json(CACHE_KEY, news, expire=CACHE_TTL)
    return news
