from __future__ import annotations

import json
import pytest

from app.core.redis import redis_client


@pytest.mark.asyncio
async def test_market_price(client):
    await redis_client.set_json("price:BTCUSDT", {"symbol": "BTCUSDT", "price": 12345.0, "timestamp": "2023-01-01T00:00:00"})
    response = await client.get("/market/price", params={"symbol": "BTCUSDT"})
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 12345.0
