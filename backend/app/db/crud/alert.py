"""Alert CRUD operations."""
from __future__ import annotations

from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.base import CRUDBase
from app.db.models.alert import Alert


class CRUDAlert(CRUDBase[Alert]):
    async def list_by_user(self, session: AsyncSession, user_id: int) -> Iterable[Alert]:
        result = await session.execute(select(Alert).where(Alert.user_id == user_id))
        return result.scalars().all()


alert = CRUDAlert(Alert)
