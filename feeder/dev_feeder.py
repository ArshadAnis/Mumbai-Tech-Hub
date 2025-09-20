"""Development price feeder generating synthetic ticks."""
from __future__ import annotations

import asyncio
import json
import random
from datetime import datetime

from redis import asyncio as redis_async

SYMBOLS = {
    "BTCUSDT": 30000.0,
    "ETHUSDT": 2000.0,
    "SOLUSDT": 20.0,
    "EURUSD": 1.1,
    "GBPUSD": 1.25,
    "USDJPY": 140.0,
}

REDIS_URL = "redis://redis:6379/0"
TIMEFRAME = "1m"
MAX_CANDLES = 500


async def publish_ticks(redis: redis_async.Redis) -> None:
    prices = SYMBOLS.copy()
    while True:
        now = datetime.utcnow().isoformat()
        for symbol, price in prices.items():
            drift = random.uniform(-0.5, 0.5)
            price = max(0.1, price * (1 + drift / 100))
            prices[symbol] = price
            data = {
                "symbol": symbol,
                "price": round(price, 2),
                "timestamp": now,
            }
            await redis.set(f"price:{symbol}", json.dumps(data))
            candle = f"{now},{price},{price},{price},{price},1"
            key = f"kline:{symbol}:{TIMEFRAME}"
            await redis.lpush(key, candle)
            await redis.ltrim(key, 0, MAX_CANDLES - 1)
        await asyncio.sleep(1)


async def main() -> None:
    redis = await redis_async.from_url(REDIS_URL)
    async with redis:
        await publish_ticks(redis)


if __name__ == "__main__":
    asyncio.run(main())
