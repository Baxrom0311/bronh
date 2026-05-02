from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from jwt.exceptions import PyJWTError as JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, decode_token, get_password_hash, verify_password
from app.models.auth_session import AuthSession
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LogoutRequest,
    LogoutResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserRead,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _is_session_expired(session: AuthSession) -> bool:
    expires_at = session.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)
    return expires_at <= _utc_now()


def _revoke_session(db: Session, session: AuthSession) -> None:
    if session.is_revoked:
        return
    session.is_revoked = True
    session.revoked_at = _utc_now()
    db.add(session)


def _issue_token_pair(db: Session, user: User) -> TokenResponse:
    session = AuthSession(
        user_id=user.id,
        expires_at=_utc_now() + timedelta(days=settings.refresh_token_expire_days),
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    access_token = create_access_token(subject=user.id, role=user.role.value)
    refresh_token = create_refresh_token(subject=user.id, role=user.role.value, session_id=session.id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, user=user)


def _resolve_refresh_session(db: Session, refresh_token: str) -> tuple[AuthSession, User]:
    try:
        payload = decode_token(refresh_token)
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

    if payload.get("type") != "refresh" or "jti" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token required")

    session = db.get(AuthSession, payload["jti"])
    if session is None or session.is_revoked or _is_session_expired(session):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh session is invalid or expired")

    user = db.get(User, payload["sub"])
    if user is None or not user.is_active or session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

    return session, user


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Yangi user ro'yxatdan o'tkazish")
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> User:
    existing_user = db.scalar(select(User).where(User.email == payload.email))
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        role=payload.role,
        preferred_language=payload.preferred_language,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse, summary="Login va access/refresh token olish")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email))
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return _issue_token_pair(db, user)


@router.post("/refresh", response_model=TokenResponse, summary="Refresh token orqali yangi token juftligini olish")
def refresh_tokens(payload: RefreshRequest, db: Session = Depends(get_db)) -> TokenResponse:
    session, user = _resolve_refresh_session(db, payload.refresh_token)
    _revoke_session(db, session)
    db.commit()
    return _issue_token_pair(db, user)


@router.post("/logout", response_model=LogoutResponse, summary="Refresh sessionni bekor qilish")
def logout(payload: LogoutRequest, db: Session = Depends(get_db)) -> LogoutResponse:
    session, _ = _resolve_refresh_session(db, payload.refresh_token)
    _revoke_session(db, session)
    db.commit()
    return LogoutResponse(message="Session revoked")


@router.get("/me", response_model=UserRead, summary="Joriy foydalanuvchini olish")
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
