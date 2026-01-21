from __future__ import annotations

from app.common.security import hash_password, verify_password
from app.config import settings

USERS = {
    "admin": {
        "password_hash": hash_password("admin"),
        "scopes": [settings.SCOPE_BOOKS_READ, settings.SCOPE_BOOKS_WRITE],
    },
    "reader": {
        "password_hash": hash_password("reader"),
        "scopes": [settings.SCOPE_BOOKS_READ],
    },
}


def authenticate_user(username: str, password: str) -> list[str] | None:
    user = USERS.get(username)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return list(user["scopes"])
