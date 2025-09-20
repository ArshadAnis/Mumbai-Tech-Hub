"""Websocket router registration."""
from fastapi import APIRouter

from app.ws import price

ws_router = APIRouter()
ws_router.include_router(price.router)
