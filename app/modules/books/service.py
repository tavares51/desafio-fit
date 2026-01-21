from __future__ import annotations

from datetime import date
from typing import Optional, List

from sqlalchemy.orm import Session

from app.common.errors import NotFoundError
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
        date_publish: Optional[date] = None,
        cover_url: Optional[str] = None,
    ) -> BookModel:
        return self.repo.create(
            db,
            title=title,
            author=author,
            date_publish=date_publish,
            cover_url=cover_url,
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
