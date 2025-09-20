"""Market data routes."""
from __future__ import annotations

from fastapi import APIRouter, Query

from app.core.rate_limit import rate_limit
from app.db.schemas.market import CandleResponse, Price, Symbol
from app.services.pricing import pricing_service

router = APIRouter()


@router.get("/symbols", response_model=list[Symbol])
async def list_symbols(market: str | None = Query(None, pattern="^(CRYPTO|FOREX)$")):
    await rate_limit("market:symbols")
    symbols = await pricing_service.list_symbols(market)
    return symbols


@router.get("/price", response_model=Price)
async def get_price(symbol: str = Query(..., min_length=3, max_length=15)):
    await rate_limit(f"market:price:{symbol}")
    return await pricing_service.get_price(symbol)


@router.get("/ohlc", response_model=CandleResponse)
async def get_ohlc(symbol: str, tf: str = "1m", limit: int = Query(200, ge=1, le=500)):
    await rate_limit(f"market:ohlc:{symbol}:{tf}")
    candles = await pricing_service.get_ohlc(symbol, tf, limit)
    return {"symbol": symbol, "timeframe": tf, "candles": candles}
