"""Email service stub for password resets and alerts."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def send_reset_email(email: str, token: str) -> None:
    logger.info("Password reset email queued for %s with token %s", email, token)
