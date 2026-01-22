# app/config.py
from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator


class Settings(BaseSettings):
    # App
    APP_NAME: str = Field(default="Books API")
    APP_VERSION: str = Field(default="0.1.0")
    DEBUG: bool = Field(default=False)

    # Database
    DATABASE_URL: str = Field(default="")
    SUPABASE_DB_URL: str = Field(default="")
    DB_USER: str = Field(default="")
    DB_PASSWORD: str = Field(default="")
    DB_HOST: str = Field(default="")
    DB_PORT: str = Field(default="5432")
    DB_NAME: str = Field(default="")

    # Supabase
    SUPABASE_URL: str = Field(default="")
    SUPABASE_ANON_KEY: str = Field(default="")
    SUPABASE_SERVICE_ROLE_KEY: str = Field(default="")
    SUPABASE_BUCKET: str = Field(default="livros")

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

    @model_validator(mode="after")
    def normalize_database_url(self) -> "Settings":
        db_url = self.DATABASE_URL or self.SUPABASE_DB_URL
        if db_url.startswith("DATABASE_URL="):
            db_url = db_url.split("=", 1)[1]
        if not db_url and self.DB_HOST:
            db_url = (
                "postgresql+psycopg2://"
                f"{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        if not db_url:
            db_url = "sqlite:///./local.db"
        if db_url.startswith("postgresql") and "sslmode=" not in db_url:
            separator = "&" if "?" in db_url else "?"
            db_url = f"{db_url}{separator}sslmode=require"
        self.DATABASE_URL = db_url
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
