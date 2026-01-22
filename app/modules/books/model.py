from sqlalchemy import String, Date, Integer
from datetime import date
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    author: Mapped[str] = mapped_column(String(120), nullable=False)
    date_publish: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    resume: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    cover_url: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True)
