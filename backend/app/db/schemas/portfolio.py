"""Portfolio schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PortfolioPositionBase(BaseModel):
    symbol: str
    quantity: float
    entry_price: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


class PortfolioPositionCreate(PortfolioPositionBase):
    pass


class PortfolioPositionOut(PortfolioPositionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PortfolioSummary(BaseModel):
    total_value: float
    profit_loss: float
    allocations: dict[str, float]
