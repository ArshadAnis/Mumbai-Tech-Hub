"""AI signals endpoint."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.config import settings
from app.core.security import get_current_active_user
from app.db.schemas.signals import SignalOut
from app.services.ai import ai_service

router = APIRouter()


@router.get("", response_model=list[SignalOut])
async def list_signals(
    symbol: str | None = Query(None),
    market: str | None = Query(None),
    user=Depends(get_current_active_user),
):
    symbols = []
    if symbol:
        symbols = [symbol]
    elif market == "FOREX":
        symbols = settings.price_symbols_forex
    else:
        symbols = settings.price_symbols_crypto

    tier_limits = {"Free": settings.max_free_signals_per_day, "Pro": 50, "Elite": 200}
    limit = tier_limits.get(user.tier, settings.max_free_signals_per_day)
    if len(symbols) > limit:
        raise HTTPException(status_code=403, detail="Signal request exceeds tier allowance.")
    return ai_service.list_signals(symbols)[:limit]
