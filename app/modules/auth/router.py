from fastapi import APIRouter, HTTPException, status

from app.common.security import create_access_token
from app.modules.auth.schemas import LoginIn, TokenOut
from app.modules.auth.service import authenticate_user

router = APIRouter()


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn):
    scopes = authenticate_user(payload.username, payload.password)
    if not scopes:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas.")

    token = create_access_token(subject=payload.username, scopes=scopes)
    return TokenOut(access_token=token)
