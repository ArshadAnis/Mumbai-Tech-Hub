"""Market data service for retrieving cached prices and candles."""
from __future__ import annotations

from datetime import datetime
from typing import List

from app.core.config import settings
from app.core.redis import redis_client


class PricingService:
    async def list_symbols(self, market: str | None = None) -> List[dict[str, str]]:
        symbols = []
        if market in (None, "CRYPTO"):
            symbols.extend(
                {"symbol": sym, "market": "CRYPTO", "description": f"Crypto pair {sym}"}
                for sym in settings.price_symbols_crypto
            )
        if market in (None, "FOREX"):
            symbols.extend(
                {"symbol": sym, "market": "FOREX", "description": f"Forex pair {sym}"}
                for sym in settings.price_symbols_forex
            )
        return symbols

    async def get_price(self, symbol: str) -> dict[str, str | float]:
        data = await redis_client.get_json(f"price:{symbol}")
        if not data:
            return {"symbol": symbol, "price": 0.0, "timestamp": datetime.utcnow().isoformat()}
        return data

    async def get_ohlc(self, symbol: str, timeframe: str, limit: int) -> list[dict[str, float | str]]:
        redis = redis_client.client
        key = f"kline:{symbol}:{timeframe}"
        raw_candles = await redis.lrange(key, 0, limit - 1)
        candles: list[dict[str, float | str]] = []
        for entry in reversed(raw_candles):
            ts, o, h, l, c, v = entry.split(",")
            candles.append(
                {
                    "timestamp": datetime.fromisoformat(ts).isoformat(),
                    "open": float(o),
                    "high": float(h),
                    "low": float(l),
                    "close": float(c),
                    "volume": float(v),
                }
            )
        return candles


pricing_service = PricingService()
