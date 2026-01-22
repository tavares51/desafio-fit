from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings
from app.common.errors import UnauthorizedError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, subject: str) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(
            (now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MIN)).timestamp()
        ),
    }
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError as e:
        raise UnauthorizedError(
            "Token inválido ou expirado.",
            {"reason": str(e)},
        ) from e


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict[str, Any]:
    """
    Valida JWT simples (Bearer).
    """
    if credentials is None:
        raise UnauthorizedError("Token não informado.")

    payload = decode_token(credentials.credentials)

    subject = payload.get("sub")
    if not subject:
        raise UnauthorizedError("Token sem subject (sub).")

    return {"username": subject}
