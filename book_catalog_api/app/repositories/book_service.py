from __future__ import annotations

import logging
from datetime import date
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.book_model import Book

logger = logging.getLogger(__name__)


def create_book_in_db(
    db: Session,
    titulo: str,
    autor: str,
    data_publicacao: Optional[date] = None,
    resumo: Optional[str] = None,
):
    """Cria um novo livro no banco de dados"""
    try:
        db_book = Book(
            titulo=titulo, autor=autor, data_publicacao=data_publicacao, resumo=resumo
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except SQLAlchemyError as e:
        logger.error(f"Database error creating book: {e}")
        raise
    except Exception as e:
        logger.error(f"Error creating book: {e}")
        raise
