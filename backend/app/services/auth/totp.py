"""TOTP helper stub."""
from __future__ import annotations

import base64
import os


def generate_secret() -> str:
    return base64.b32encode(os.urandom(10)).decode("utf-8")


def verify_totp(secret: str, code: str) -> bool:
    # Placeholder - integrate with pyotp
    return code == "000000"
