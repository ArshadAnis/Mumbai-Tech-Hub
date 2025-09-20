"""Compliance models."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class PrivacyExport(BaseModel):
    user_id: int
    requested_at: datetime
    data: dict


class PrivacyDeleteRequest(BaseModel):
    confirm: bool
