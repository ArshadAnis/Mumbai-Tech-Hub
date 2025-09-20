"""Placeholder AlphaVantage provider."""
from __future__ import annotations

from typing import List


def fetch_forex_quotes(symbols: List[str]) -> dict[str, float]:
    return {symbol: 0.0 for symbol in symbols}
