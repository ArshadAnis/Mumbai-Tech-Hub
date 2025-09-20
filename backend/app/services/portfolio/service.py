"""Portfolio analytics helpers."""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from app.db.models.portfolio import PortfolioPosition


def summarise_positions(positions: Iterable[PortfolioPosition]) -> dict[str, float | dict[str, float]]:
    total_value = 0.0
    allocations: dict[str, float] = defaultdict(float)
    for pos in positions:
        value = float(pos.quantity) * float(pos.entry_price)
        total_value += value
        allocations[pos.symbol] += value
    if total_value > 0:
        allocations = {symbol: value / total_value for symbol, value in allocations.items()}
    else:
        allocations = {symbol: 0.0 for symbol in allocations}
    return {
        "total_value": total_value,
        "profit_loss": 0.0,
        "allocations": allocations,
    }
