"""Lifecycle event handlers."""
from __future__ import annotations

import logging
from typing import Callable

from fastapi import FastAPI

from app.core.config import settings
from app.core.redis import redis_client
from app.db.session import engine
from app.db import init_db


logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI) -> Callable[[], None]:
    async def start_app() -> None:
        logger.info("Starting Money Trader API in %s mode", settings.environment)
        await init_db.run_migrations()
        await init_db.seed_defaults()
        await redis_client.connect()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable[[], None]:
    async def stop_app() -> None:
        await redis_client.disconnect()
        await engine.dispose()
        logger.info("Application shutdown complete")

    return stop_app
