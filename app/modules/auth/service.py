from __future__ import annotations

from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt

from app.config import settings
from app.common.security import hash_password, verify_password

_FAKE_USERS = {
    "admin": {
        "username": "admin",
        "password_hash": hash_password("admin"),
        "scopes": [settings.SCOPE_BOOKS_READ, settings.SCOPE_BOOKS_WRITE],
    },
    "reader": {
        "username": "reader",
        "password_hash": hash_password("reader"),
        "scopes": [settings.SCOPE_BOOKS_READ],
    },
}

def authenticate_user(username: str, password: str) -> dict:
    user = _FAKE_USERS.get(username)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return user

def create_access_token(subject: str, scopes: list[str]) -> str:
    exp = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MIN)
    payload = {"sub": subject, "exp": exp, "scopes": scopes}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
