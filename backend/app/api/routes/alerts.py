"""Alert endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import get_current_active_user
from app.db.crud import alert as crud_alert
from app.db.schemas.alert import AlertCreate, AlertOut

router = APIRouter()


@router.get("", response_model=list[AlertOut])
async def list_alerts(user=Depends(get_current_active_user), session: AsyncSession = Depends(get_db)):
    return await crud_alert.alert.list_by_user(session, user.id)


@router.post("", response_model=AlertOut)
async def create_alert(
    payload: AlertCreate,
    user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    existing = await crud_alert.alert.list_by_user(session, user.id)
    tier_limits = {
        "Free": settings.max_free_alerts,
        "Pro": 25,
        "Elite": 100,
    }
    limit = tier_limits.get(user.tier, settings.max_free_alerts)
    if len(existing) >= limit:
        raise HTTPException(status_code=403, detail="Alert limit reached. Upgrade your tier for more alerts.")
    data = payload.dict()
    data.update({"user_id": user.id})
    alert = await crud_alert.alert.create(session, data)
    return alert


@router.delete("/{alert_id}", status_code=204)
async def delete_alert(alert_id: int, user=Depends(get_current_active_user), session: AsyncSession = Depends(get_db)):
    alert = await crud_alert.alert.get(session, alert_id)
    if not alert or alert.user_id != user.id:
        raise HTTPException(status_code=404, detail="Alert not found")
    await crud_alert.alert.remove(session, id=alert_id)
    return None


@router.post("/test/{alert_id}")
async def test_alert(alert_id: int, user=Depends(get_current_active_user), session: AsyncSession = Depends(get_db)):
    alert = await crud_alert.alert.get(session, alert_id)
    if not alert or alert.user_id != user.id:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"alert_id": alert_id, "message": "Test notification dispatched"}
