"""Security utilities including JWT and password hashing."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Optional

import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.hash import argon2

from app.core.config import settings
from app.db.crud import user as crud_user
from app.db.session import async_session


security_scheme = HTTPBearer(auto_error=False)


def get_password_hash(password: str) -> str:
    return argon2.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return argon2.verify(plain_password, hashed_password)


def _create_token(subject: str, expires_delta: timedelta) -> str:
    payload = {
        "sub": subject,
        "exp": datetime.utcnow() + expires_delta,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str) -> str:
    return _create_token(subject, timedelta(minutes=settings.jwt_access_expire_minutes))


def create_refresh_token(subject: str) -> str:
    return _create_token(subject, timedelta(minutes=settings.jwt_refresh_expire_minutes))


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
) -> Any:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:  # pragma: no cover - jwt library handles message
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    user_id = int(payload.get("sub"))
    async with async_session() as session:
        db_user = await crud_user.user.get(session, user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        if not db_user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive")
        return db_user


async def get_current_active_user(user=Depends(get_current_user)):
    return user


async def get_current_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return user
