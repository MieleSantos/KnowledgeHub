from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """Esquema base para um livro, contendo os campos essenciais"""

    titulo: str = Field(
        ..., description="Título do livro", example="O Senhor dos Anéis"
    )
    autor: str = Field(..., description="Autor do livro", example="J.R.R. Tolkien")
    data_publicacao: Optional[date] = Field(
        None, description="Data de publicação do livro", example="1954-07-29"
    )
    resumo: Optional[str] = Field(
        None, description="Resumo do livro", example="Uma épica aventura..."
    )


class BookCreate(BookBase):
    """Schema para criação de livro"""

    pass


class BookResponse(BookBase):
    """Esquema de resposta para um livro"""

    id: int = Field(..., description="ID do livro", example=1)

    class Config:
        from_attributes = True
