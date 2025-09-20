"""Database initialisation helpers."""
from __future__ import annotations

import logging

from sqlalchemy import text

from app.db.session import engine

logger = logging.getLogger(__name__)


async def run_migrations() -> None:
    """Placeholder for Alembic integration; executes simple sanity check."""
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
        logger.info("Database connectivity verified")


async def seed_defaults() -> None:
    """Seed minimal lookup data for tiers if missing."""
    async with engine.begin() as conn:
        await conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS billing_tiers (
                    name TEXT PRIMARY KEY,
                    price NUMERIC,
                    features JSONB,
                    created_at TIMESTAMP DEFAULT NOW()
                )
                """
            )
        )
        await conn.execute(
            text(
                """
                INSERT INTO billing_tiers (name, price, features)
                VALUES
                    ('Free', 0, '{"alerts":3,"signals":3}'),
                    ('Pro', 29, '{"alerts":25,"signals":50}'),
                    ('Elite', 79, '{"alerts":100,"signals":200}')
                ON CONFLICT (name) DO NOTHING
                """
            )
        )
        logger.info("Billing tiers seeded")
