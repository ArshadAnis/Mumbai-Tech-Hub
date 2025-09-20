"""Mock economic calendar provider."""
from __future__ import annotations

from datetime import datetime
from typing import List

from app.core.redis import redis_client

CACHE_KEY = "calendar:events"
CACHE_TTL = 300


async def fetch_calendar() -> List[dict[str, str]]:
    cached = await redis_client.get_json(CACHE_KEY)
    if cached:
        return cached
    events = [
        {
            "event": "FOMC Statement",
            "impact": "High",
            "time": datetime.utcnow().isoformat(),
            "disclaimer": "Economic data subject to change.",
        }
    ]
    await redis_client.set_json(CACHE_KEY, events, expire=CACHE_TTL)
    return events
