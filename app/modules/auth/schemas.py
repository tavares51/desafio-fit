from pydantic import BaseModel, Field


class LoginIn(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=2, max_length=100)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
