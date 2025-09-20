"""Main entrypoint for Money Trader FastAPI application."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.ws import ws_router


def get_application() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="Money Trader API",
        description=(
            "Signals and alerts platform for crypto and forex traders. "
            "Not financial advice. Trading involves risk."
        ),
        version=settings.version,
        docs_url="/docs" if settings.dev_mode else None,
        redoc_url="/redoc" if settings.dev_mode else None,
        openapi_tags=[
            {"name": "health", "description": "Service availability checks."},
            {"name": "market", "description": "Market data endpoints."},
            {"name": "auth", "description": "Authentication and user management."},
            {"name": "portfolio", "description": "Portfolio tracking endpoints."},
            {"name": "alerts", "description": "Alert management endpoints."},
            {"name": "signals", "description": "AI-assisted strategy signals."},
            {"name": "billing", "description": "Subscription tiers and webhooks."},
            {"name": "compliance", "description": "Privacy and audit utilities."},
            {"name": "admin", "description": "Administrative insights."},
        ],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", create_start_app_handler(app))
    app.add_event_handler("shutdown", create_stop_app_handler(app))

    app.include_router(api_router)
    app.include_router(ws_router)

    return app


app = get_application()
