from __future__ import annotations

from fastapi import APIRouter
from app.modules.auth.schemas import LoginIn, TokenOut
from app.modules.auth.service import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn) -> TokenOut:
    authenticate_user(payload.username, payload.password)
    token = create_access_token(payload.username)
    return TokenOut(access_token=token)
