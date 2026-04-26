"""Schemas para busca semântica."""

from pydantic import BaseModel


class Document(BaseModel):
    """Schema para um documento.

    Attributes:
        id: Identificador único do documento.
        title: Título do documento.
        content: Conteúdo do documento.
    """

    id: str
    title: str
    content: str


class SearchResult(BaseModel):
    """Schema para resultado de busca.

    Attributes:
        id: Identificador único do documento.
        title: Título do documento.
        content: Conteúdo do documento.
        score: Score de similaridade.
    """

    id: str
    title: str
    content: str
    score: float
