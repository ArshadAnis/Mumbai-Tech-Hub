"""Billing and subscription endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.db.schemas.billing import BillingWebhook, Tier

router = APIRouter()


@router.get("/tiers", response_model=list[Tier])
async def list_tiers(session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT name, price, features FROM billing_tiers"))
    rows = result.fetchall()
    return [Tier(name=row.name, price=float(row.price), features=row.features) for row in rows]


@router.post("/webhook")
async def billing_webhook(payload: BillingWebhook):
    return {"status": "received", "provider": payload.provider}
