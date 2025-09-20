"""Portfolio positions."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class PortfolioPosition(Base):
    __tablename__ = "portfolio_positions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String(20), nullable=False)
    quantity = Column(Numeric(18, 8), nullable=False)
    entry_price = Column(Numeric(18, 8), nullable=False)
    stop_loss = Column(Numeric(18, 8), nullable=True)
    take_profit = Column(Numeric(18, 8), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="portfolio_positions")
