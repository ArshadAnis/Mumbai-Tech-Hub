"""Authentication routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.db.crud import user as crud_user
from app.db.crud import audit as audit_crud
from app.db.schemas import auth as schemas_auth
from app.db.schemas.user import UserCreate, UserLogin, UserOut
from app.services.auth import email as email_service
from app.services.auth import totp as totp_service

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    existing = await crud_user.user.get_by_email(session, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = get_password_hash(payload.password)
    db_user = await crud_user.user.create(
        session,
        {
            "email": payload.email,
            "full_name": payload.full_name,
            "hashed_password": hashed_password,
            "tier": "Free",
        },
    )
    await audit_crud.record_audit(
        session,
        user_id=db_user.id,
        action="register",
        ip_address=request.client.host if request.client else None,
        details={"tier": db_user.tier},
    )
    return db_user


@router.post("/login", response_model=schemas_auth.Token)
async def login(
    payload: UserLogin,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    db_user = await crud_user.user.get_by_email(session, payload.email)
    if not db_user or not verify_password(payload.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(str(db_user.id))
    refresh_token = create_refresh_token(str(db_user.id))
    await audit_crud.record_audit(
        session,
        user_id=db_user.id,
        action="login",
        ip_address=request.client.host if request.client else None,
        details={"tier": db_user.tier},
    )
    return schemas_auth.Token(access_token=access_token, refresh_token=refresh_token, expires_in=settings.jwt_access_expire_minutes * 60)


@router.post("/refresh", response_model=schemas_auth.Token)
async def refresh_token(payload: schemas_auth.TokenPayload):
    access_token = create_access_token(payload.sub)
    refresh_token = create_refresh_token(payload.sub)
    return schemas_auth.Token(access_token=access_token, refresh_token=refresh_token, expires_in=settings.jwt_access_expire_minutes * 60)


@router.post("/password/forgot")
async def password_forgot(payload: schemas_auth.PasswordResetRequest, session: AsyncSession = Depends(get_db)):
    user = await crud_user.user.get_by_email(session, payload.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    token = create_refresh_token(str(user.id))
    email_service.send_reset_email(payload.email, token)
    return {"status": "ok"}


@router.post("/password/reset")
async def password_reset(payload: schemas_auth.PasswordReset, session: AsyncSession = Depends(get_db)):
    if payload.new_password != payload.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    # In real implementation validate token and update password
    return {"status": "ok"}


@router.post("/totp/setup")
async def totp_setup():
    return {"secret": totp_service.generate_secret(), "qr": "stub://qr"}


@router.post("/totp/verify")
async def totp_verify(code: str):
    if totp_service.verify_totp("", code):
        return {"verified": True}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid code")
