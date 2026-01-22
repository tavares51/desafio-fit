from __future__ import annotations

from datetime import date
from typing import Optional, Protocol, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.books.model import BookModel


class BookRepository(Protocol):
    def create(
        self,
        db: Session,
        *,
        title: str,
        author: str,
        resume: Optional[str],
        date_publish: Optional[date],
        cover_url: Optional[str] = None,
    ) -> BookModel:
        ...

    def list(self, db: Session) -> List[BookModel]:
        ...

    def get(self, db: Session, book_id: int) -> Optional[BookModel]:
        ...

    def update(self, db: Session, book: BookModel, **fields) -> BookModel:
        ...

    def delete(self, db: Session, book: BookModel) -> None:
        ...


class SqlAlchemyBookRepository:
    def create(
        self,
        db: Session,
        *,
        title: str,
        author: str,
        resume: Optional[str],
        date_publish: Optional[date],
        cover_url: Optional[str] = None,
    ) -> BookModel:
        book = BookModel(
            title=title,
            author=author,
            date_publish=date_publish,
            cover_url=cover_url,
            resume=resume,
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    def list(self, db: Session) -> List[BookModel]:
        stmt = select(BookModel).order_by(BookModel.id.desc())
        return list(db.execute(stmt).scalars().all())

    def get(self, db: Session, book_id: int) -> Optional[BookModel]:
        return db.get(BookModel, book_id)

    def update(self, db: Session, book: BookModel, **fields) -> BookModel:
        for k, v in fields.items():
            if v is not None:
                setattr(book, k, v)
        db.commit()
        db.refresh(book)
        return book

    def delete(self, db: Session, book: BookModel) -> None:
        db.delete(book)
        db.commit()
