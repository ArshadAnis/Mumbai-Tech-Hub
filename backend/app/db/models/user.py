"""User database model."""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(50), default=UserRole.USER.value)
    tier = Column(String(50), default="Free")
    totp_secret = Column(String(32), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="user")
    alerts = relationship("Alert", back_populates="user")
    portfolio_positions = relationship("PortfolioPosition", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<User email={self.email} tier={self.tier}>"
