"""Privacy and compliance endpoints."""
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends

from app.core.security import get_current_active_user
from app.db.schemas.compliance import PrivacyDeleteRequest, PrivacyExport

router = APIRouter()


@router.get("/export", response_model=PrivacyExport)
async def export_data(user=Depends(get_current_active_user)):
    return PrivacyExport(user_id=user.id, requested_at=datetime.utcnow(), data={"email": user.email, "tier": user.tier})


@router.post("/delete")
async def delete_data(payload: PrivacyDeleteRequest, user=Depends(get_current_active_user)):
    if not payload.confirm:
        return {"status": "cancelled"}
    return {"status": "scheduled", "user_id": user.id}
