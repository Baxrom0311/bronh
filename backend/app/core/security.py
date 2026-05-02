from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _create_token(subject: str, role: str, expires_delta: timedelta, token_type: str, jti: str | None = None) -> str:
    expire = datetime.now(UTC) + expires_delta
    payload = {"sub": subject, "role": role, "type": token_type, "exp": expire}
    if jti is not None:
        payload["jti"] = jti
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str, role: str) -> str:
    return _create_token(
        subject=subject,
        role=role,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        token_type="access",
    )


def create_refresh_token(subject: str, role: str, session_id: str) -> str:
    return _create_token(
        subject=subject,
        role=role,
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
        token_type="refresh",
        jti=session_id,
    )


def decode_token(token: str) -> dict[str, str]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
