from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional, List
from uuid import uuid4

from sqlalchemy.orm import Session

from app.common.errors import NotFoundError, AppError
from app.common.supabase import get_supabase_client, build_public_url
from app.config import settings
from app.modules.books.repository import BookRepository
from app.modules.books.model import BookModel


class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def create(
        self,
        db: Session,
        *,
        title: str,
        author: str,
        resume: Optional[str],
        date_publish: Optional[date] = None,
        cover_url: Optional[str] = None,
    ) -> BookModel:
        return self.repo.create(
            db,
            title=title,
            author=author,
            date_publish=date_publish,
            cover_url=cover_url,
            resume=resume,
        )

    def list(self, db: Session) -> List[BookModel]:
        return self.repo.list(db)

    def get(self, db: Session, *, book_id: int) -> BookModel:
        book = self.repo.get(db, book_id)
        if not book:
            raise NotFoundError("Livro não encontrado.", {"id": book_id})
        return book

    def update(self, db: Session, *, book_id: int, **fields) -> BookModel:
        book = self.get(db, book_id=book_id)
        return self.repo.update(db, book, **fields)

    def delete(self, db: Session, *, book_id: int) -> None:
        book = self.get(db, book_id=book_id)
        self.repo.delete(db, book)

    def upload_cover(
        self,
        db: Session,
        *,
        book_id: int,
        filename: str,
        content: bytes,
        content_type: Optional[str],
    ) -> BookModel:
        book = self.get(db, book_id=book_id)
        if not settings.SUPABASE_BUCKET:
            raise AppError("Bucket do Supabase não configurado.")

        suffix = Path(filename or "cover").suffix
        object_path = f"books/{uuid4().hex}{suffix}"

        try:
            client = get_supabase_client()
            client.storage.from_(settings.SUPABASE_BUCKET).upload(
                object_path,
                content,
                {"content-type": content_type or "application/octet-stream"},
            )
        except Exception as exc:
            raise AppError("Erro ao enviar capa.", {"detail": str(exc)})

        cover_url = build_public_url(object_path)
        return self.repo.update(db, book, cover_url=cover_url)
