"""AI signal schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class SignalOut(BaseModel):
    symbol: str
    direction: str
    confidence: float
    rationale: str
    generated_at: datetime
