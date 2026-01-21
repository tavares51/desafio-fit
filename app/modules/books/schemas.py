from __future__ import annotations

from datetime import date
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    author: str = Field(min_length=1, max_length=120)
    date_publish: Optional[date] = None
    cover_url: Optional[HttpUrl] = None


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=180)
    author: Optional[str] = Field(default=None, min_length=1, max_length=120)
    date_publish: Optional[date] = None
    cover_url: Optional[HttpUrl] = None


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    date_publish: Optional[date]
    cover_url: Optional[HttpUrl]

    class Config:
        from_attributes = True


class BooksListOut(BaseModel):
    items: List[BookOut]
