"""Deterministic AI stub using simple indicators."""
from __future__ import annotations

from datetime import datetime
from typing import List


class AIService:
    def generate_signal(self, symbol: str) -> dict[str, str | float]:
        direction = "buy" if symbol.endswith("USD") else "hold"
        confidence = 0.6 if direction == "buy" else 0.4
        rationale = "EMA crossover stub" if direction == "buy" else "Insufficient momentum"
        return {
            "symbol": symbol,
            "direction": direction,
            "confidence": confidence,
            "rationale": rationale,
            "generated_at": datetime.utcnow(),
        }

    def list_signals(self, symbols: List[str]) -> List[dict[str, str | float]]:
        return [self.generate_signal(symbol) for symbol in symbols]


ai_service = AIService()
