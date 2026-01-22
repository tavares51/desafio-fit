from __future__ import annotations

from functools import lru_cache

from supabase import Client, create_client

from app.config import settings


@lru_cache
def get_supabase_client() -> Client:
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY
    if not url or not key:
        raise RuntimeError("Supabase credentials not configured.")
    return create_client(url, key)


def build_public_url(path: str) -> str:
    if not settings.SUPABASE_URL or not settings.SUPABASE_BUCKET:
        raise RuntimeError("Supabase storage not configured.")
    return (
        f"{settings.SUPABASE_URL}/storage/v1/object/public/"
        f"{settings.SUPABASE_BUCKET}/{path}"
    )
