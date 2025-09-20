"""Async worker that periodically evaluates alerts."""
from __future__ import annotations

import asyncio
import logging

from app.core.redis import redis_client
from app.db.session import async_session
from app.services.alerts.service import evaluate_alerts

logger = logging.getLogger(__name__)


async def run_polling(interval: int = 5) -> None:
    await redis_client.connect()
    while True:
        async with async_session() as session:
            triggered = await evaluate_alerts(session)
            for alert_id in triggered:
                logger.info("Alert %s triggered", alert_id)
        await asyncio.sleep(interval)


if __name__ == "__main__":
    asyncio.run(run_polling())
