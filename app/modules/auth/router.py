from __future__ import annotations

from fastapi import APIRouter
from app.modules.auth.schemas import LoginIn, TokenOut
from app.modules.auth.service import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn) -> TokenOut:
    user = authenticate_user(payload.username, payload.password)
    token = create_access_token(user["username"], user["scopes"])
    return TokenOut(access_token=token)
