"""Alert schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AlertBase(BaseModel):
    symbol: str = Field(..., example="BTCUSDT")
    trigger_price: float
    direction: str
    timeframe: str = "1m"
    note: Optional[str] = None


class AlertCreate(AlertBase):
    pass


class AlertOut(AlertBase):
    id: int
    triggered_at: Optional[datetime]
    is_active: bool

    class Config:
        orm_mode = True
