"""Synthetic data provider used in development with the feeder."""
from __future__ import annotations

import asyncio
import random
from datetime import datetime

from app.core.redis import redis_client


SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "EURUSD", "GBPUSD", "USDJPY"]


async def push_tick(symbol: str, price: float) -> None:
    data = {
        "symbol": symbol,
        "price": price,
        "timestamp": datetime.utcnow().isoformat(),
    }
    await redis_client.set_json(f"price:{symbol}", data)


async def generate_random_walk() -> None:
    redis = redis_client.client
    prices = {symbol: random.uniform(20_000, 35_000) for symbol in SYMBOLS}
    while True:
        for symbol in SYMBOLS:
            drift = random.uniform(-0.5, 0.5)
            prices[symbol] = max(0.1, prices[symbol] * (1 + drift / 100))
            await push_tick(symbol, prices[symbol])
        await asyncio.sleep(1)
