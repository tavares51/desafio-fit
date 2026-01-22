from __future__ import annotations

from fastapi import APIRouter, Depends, Security, status, UploadFile, File
from sqlalchemy.orm import Session

from app.config import settings
from app.db.session import get_db
from app.common.security import get_current_user
from app.modules.books.schemas import BookCreate, BookUpdate, BookOut, BooksListOut
from app.modules.books.repository import SqlAlchemyBookRepository
from app.modules.books.service import BookService

router = APIRouter()

_service = BookService(repo=SqlAlchemyBookRepository())


@router.get("", response_model=BooksListOut)
def list_books(
    db: Session = Depends(get_db),
    _user=Security(get_current_user, scopes=[settings.SCOPE_BOOKS_READ]),
):
    items = _service.list(db)
    return {"items": items}


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(
    payload: BookCreate,
    db: Session = Depends(get_db),
    _user=Security(get_current_user, scopes=[settings.SCOPE_BOOKS_WRITE]),
):
    data = payload.model_dump()
    if data.get("cover_url") is not None:
        data["cover_url"] = str(data["cover_url"])
    book = _service.create(db, **data)
    return book


@router.get("/{book_id}", response_model=BookOut)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    _user=Security(get_current_user, scopes=[settings.SCOPE_BOOKS_READ]),
):
    return _service.get(db, book_id=book_id)


@router.patch("/{book_id}", response_model=BookOut)
def update_book(
    book_id: int,
    payload: BookUpdate,
    db: Session = Depends(get_db),
    _user=Security(get_current_user, scopes=[settings.SCOPE_BOOKS_WRITE]),
):
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if data.get("cover_url") is not None:
        data["cover_url"] = str(data["cover_url"])
    return _service.update(db, book_id=book_id, **data)


@router.post("/{book_id}/cover", response_model=BookOut)
def upload_book_cover(
    book_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _user=Security(get_current_user, scopes=[settings.SCOPE_BOOKS_WRITE]),
):
    try:
        content = file.file.read()
    finally:
        file.file.close()
    return _service.upload_cover(
        db,
        book_id=book_id,
        filename=file.filename or "cover",
        content=content,
        content_type=file.content_type,
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    _user=Security(get_current_user, scopes=[settings.SCOPE_BOOKS_WRITE]),
):
    _service.delete(db, book_id=book_id)
    return None
