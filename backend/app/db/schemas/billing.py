"""Billing schemas."""
from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel


class Tier(BaseModel):
    name: str
    price: float
    features: Dict[str, int]


class BillingWebhook(BaseModel):
    provider: str
    payload: Dict[str, str]
