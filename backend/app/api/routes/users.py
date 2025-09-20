"""Current user endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.security import get_current_active_user
from app.db.schemas.user import UserMe

router = APIRouter()


@router.get("", response_model=UserMe)
async def get_me(user=Depends(get_current_active_user)):
    tier_limits = {
        "Free": (settings.max_free_alerts, settings.max_free_signals_per_day),
        "Pro": (25, 50),
        "Elite": (100, 200),
    }
    alerts, signals = tier_limits.get(user.tier, (settings.max_free_alerts, settings.max_free_signals_per_day))
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "tier": user.tier,
        "is_verified": user.is_verified,
        "created_at": user.created_at,
        "alert_limit": alerts,
        "signal_limit": signals,
    }
