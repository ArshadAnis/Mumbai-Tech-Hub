"""Market data schemas."""
from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel


class Symbol(BaseModel):
    symbol: str
    market: str
    description: str


class Price(BaseModel):
    symbol: str
    price: float
    timestamp: datetime


class Candle(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float | None = None


class CandleResponse(BaseModel):
    symbol: str
    timeframe: str
    candles: List[Candle]
