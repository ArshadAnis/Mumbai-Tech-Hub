"""Placeholder Binance provider to be implemented with official APIs."""
from __future__ import annotations

from typing import AsyncIterator


async def stream_prices(symbols: list[str]) -> AsyncIterator[dict[str, str | float]]:
    """Yield placeholder data until real integration is provided."""
    for symbol in symbols:
        yield {"symbol": symbol, "price": 0.0}
