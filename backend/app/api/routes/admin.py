"""Admin-only endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_admin

router = APIRouter()


@router.get("/stats")
async def admin_stats(user=Depends(get_current_admin), session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT COUNT(*) FROM users"))
    users_count = result.scalar() or 0
    return {"users": users_count, "environment": "dev"}
