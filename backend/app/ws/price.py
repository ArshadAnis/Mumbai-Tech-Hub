"""WebSocket price stream endpoint."""
from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.redis import redis_client

router = APIRouter()


@router.websocket("/ws/price")
async def price_stream(websocket: WebSocket, symbols: str) -> None:
    await websocket.accept()
    symbol_list = [sym.strip().upper() for sym in symbols.split(",") if sym.strip()]
    try:
        while True:
            payload = {}
            for symbol in symbol_list:
                price = await redis_client.get_json(f"price:{symbol}")
                if price:
                    payload[symbol] = price
            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        await websocket.close()
