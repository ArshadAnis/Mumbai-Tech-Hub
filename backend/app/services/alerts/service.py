"""Alert helper functions."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis_client
from app.db.crud import alert as crud_alert


async def evaluate_alerts(session: AsyncSession) -> list[int]:
    triggered_ids: list[int] = []
    alerts = await crud_alert.alert.list(session, skip=0, limit=1000)
    for alert in alerts:
        if not alert.is_active or alert.triggered_at:
            continue
        price_data = await redis_client.get_json(f"price:{alert.symbol}")
        if not price_data:
            continue
        price = float(price_data["price"])
        if alert.direction == "above" and price >= float(alert.trigger_price):
            alert.triggered_at = datetime.utcnow()
            alert.is_active = 0
        elif alert.direction == "below" and price <= float(alert.trigger_price):
            alert.triggered_at = datetime.utcnow()
            alert.is_active = 0
        else:
            continue
        triggered_ids.append(alert.id)
    if triggered_ids:
        await session.commit()
    return triggered_ids
