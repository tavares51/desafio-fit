# app/config.py
from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # App
    APP_NAME: str = Field(default="Books API")
    APP_VERSION: str = Field(default="0.1.0")
    DEBUG: bool = Field(default=False)

    # Database
    DATABASE_URL: str = Field(default="sqlite:///./local.db")

    # JWT
    JWT_SECRET_KEY: str = Field(default="change-me")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_ACCESS_TOKEN_EXPIRES_MIN: int = Field(default=60)

    # Scopes
    SCOPE_BOOKS_READ: str = "books:read"
    SCOPE_BOOKS_WRITE: str = "books:write"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
