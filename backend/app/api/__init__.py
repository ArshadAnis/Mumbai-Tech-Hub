"""FastAPI router registrations."""
from fastapi import APIRouter

from app.api.routes import (
    admin,
    alerts,
    auth,
    billing,
    compliance,
    content,
    health,
    market,
    portfolio,
    signals,
    users,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(content.router, tags=["market"])
api_router.include_router(market.router, prefix="/market", tags=["market"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/me", tags=["auth"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(signals.router, prefix="/signals", tags=["signals"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
api_router.include_router(compliance.router, prefix="/privacy", tags=["compliance"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
