"""Audit helper to record events."""
from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.audit import AuditLog


async def record_audit(
    session: AsyncSession,
    *,
    user_id: int | None,
    action: str,
    ip_address: str | None,
    details: dict[str, Any] | None = None,
) -> None:
    log = AuditLog(user_id=user_id, action=action, ip_address=ip_address, details=details)
    session.add(log)
    await session.commit()
