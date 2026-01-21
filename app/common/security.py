from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings
from app.common.errors import UnauthorizedError, ForbiddenError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 com scopes aparece automaticamente no Swagger (/docs)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes={
        settings.SCOPE_BOOKS_READ: "Permite leitura de livros",
        settings.SCOPE_BOOKS_WRITE: "Permite criar/editar/remover livros",
    },
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, subject: str, scopes: list[str]) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "scopes": scopes,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MIN)).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as e:
        raise UnauthorizedError("Token inválido ou expirado.", {"reason": str(e)}) from e


def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    """
    Valida o JWT e checa scopes exigidos na rota.
    Retorna um dict com dados do usuário (mínimo necessário).
    """
    payload = decode_token(token)

    subject = payload.get("sub")
    token_scopes = payload.get("scopes", [])

    if not subject:
        raise UnauthorizedError("Token sem subject (sub).")

    required = set(security_scopes.scopes or [])
    owned = set(token_scopes or [])
    missing = sorted(required - owned)
    if missing:
        raise ForbiddenError("Escopo insuficiente.", {"missing_scopes": missing})

    return {"username": subject, "scopes": list(owned)}
