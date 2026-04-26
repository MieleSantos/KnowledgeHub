from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.book_model import Book
from app.repositories.book_service import create_book_in_db
from app.schemas.book_schemas import BookCreate, BookResponse

router = APIRouter()


class PaginatedBooksResponse(BaseModel):
    items: list[BookResponse]
    total: int
    page: int
    size: int
    pages: int


@router.post(
    "/books/", response_model=BookResponse, status_code=status.HTTP_201_CREATED
)
async def create_book(book: BookCreate, db: Session = Depends(get_db)) -> BookResponse:
    return create_book_in_db(
        db,
        titulo=book.titulo,
        autor=book.autor,
        data_publicacao=book.data_publicacao,
        resumo=book.resumo,
    )


@router.get(
    "/books/", response_model=PaginatedBooksResponse, status_code=status.HTTP_200_OK
)
async def list_books(
    page: int = 1,
    size: int = 10,
    q: str | None = None,
    db: Session = Depends(get_db),
) -> PaginatedBooksResponse:
    query = db.query(Book)

    if q:
        query = query.filter(
            func.lower(Book.titulo).like(f"%{q.lower()}%")
            | func.lower(Book.autor).like(f"%{q.lower()}%")
        )

    total = query.count()
    pages = (total + size - 1) // size if total > 0 else 1
    items = query.offset((page - 1) * size).limit(size).all()

    return PaginatedBooksResponse(
        items=[BookResponse.model_validate(b) for b in items],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get(
    "/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK
)
async def get_book(book_id: int, db: Session = Depends(get_db)) -> BookResponse:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return BookResponse.model_validate(book)
