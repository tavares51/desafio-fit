from __future__ import annotations

from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt

from app.config import settings
from app.common.security import hash_password, verify_password

_FAKE_USER = {
    "username": "admin",
    "password_hash": hash_password("admin"),
}

def authenticate_user(username: str, password: str) -> None:
    if username != _FAKE_USER["username"]:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    if not verify_password(password, _FAKE_USER["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

def create_access_token(subject: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MIN)
    payload = {"sub": subject, "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
