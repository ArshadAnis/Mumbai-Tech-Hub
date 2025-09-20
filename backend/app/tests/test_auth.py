from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_register_requires_unique_email(client):
    payload = {"email": "test@example.com", "password": "secret123", "full_name": "Test"}
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 201
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 400
