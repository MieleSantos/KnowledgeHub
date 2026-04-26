from sqlalchemy import Column, Date, Integer, String

from app.core.database import Base


class Book(Base):
    "Modelo de banco de dados para um livro, representando a tabela 'books'"

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(255), index=True, nullable=False)
    autor = Column(String(255), index=True, nullable=False)
    data_publicacao = Column(Date)
    resumo = Column(String)

    def __repr__(self):
        return f"<Book id={self.id} titulo='{self.titulo}'>"
