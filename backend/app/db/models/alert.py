"""Price alert model."""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class AlertDirection(str, Enum):
    ABOVE = "above"
    BELOW = "below"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    symbol = Column(String(20), nullable=False)
    trigger_price = Column(Numeric(18, 8), nullable=False)
    direction = Column(String(10), nullable=False)
    timeframe = Column(String(10), nullable=False, default="1m")
    note = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    triggered_at = Column(DateTime, nullable=True)
    is_active = Column(Integer, default=1)

    user = relationship("User", back_populates="alerts")
