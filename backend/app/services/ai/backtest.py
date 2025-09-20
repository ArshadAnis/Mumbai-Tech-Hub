"""Backtest harness placeholder."""
from __future__ import annotations

from typing import Iterable, List


def run_backtest(prices: Iterable[float]) -> dict[str, float]:
    returns = list(prices)
    if not returns:
        return {"roi": 0.0}
    roi = (returns[-1] - returns[0]) / returns[0] if returns[0] else 0.0
    return {"roi": roi}
