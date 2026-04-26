from fastapi import status

API = "/api/v1"


def test_create_book_minimal(client):
    """
    Cria um livro com apenas os campos obrigatórios
    e verifica se os dados retornados estão corretos.
    """
    payload = {"titulo": "Duna", "autor": "Frank Herbert"}
    r = client.post(f"{API}/books/", json=payload)
    assert r.status_code == status.HTTP_201_CREATED
    data = r.json()
    assert data["id"] >= 1
    assert data["titulo"] == "Duna"
    assert data["autor"] == "Frank Herbert"
    assert data["data_publicacao"] is None
    assert data["resumo"] is None


def test_create_book_full(client):
    """
    Cria um livro com todos os campos preenchidos
    e verifica se os dados retornados estão corretos.
    """
    payload = {
        "titulo": "O Senhor dos Anéis",
        "autor": "J.R.R. Tolkien",
        "data_publicacao": "1954-07-29",
        "resumo": "Uma épica aventura na Terra Média.",
    }
    r = client.post(f"{API}/books/", json=payload)
    assert r.status_code == status.HTTP_201_CREATED
    data = r.json()
    assert data["titulo"] == payload["titulo"]
    assert data["autor"] == payload["autor"]
    assert data["data_publicacao"] == "1954-07-29"
    assert data["resumo"] == payload["resumo"]


def test_list_books_empty(client):
    """
    Verifica se a listagem de livros retorna uma lista vazia
    quando não há livros cadastrados.
    """
    r = client.get(f"{API}/books/")
    assert r.status_code == status.HTTP_200_OK
    assert r.json() == []


def test_list_books_after_create(client):
    """Cria dois livros e depois verifica se eles aparecem na listagem geral"""
    client.post(
        f"{API}/books/",
        json={"titulo": "Livro A", "autor": "Autor X"},
    )
    client.post(
        f"{API}/books/",
        json={"titulo": "Livro B", "autor": "Autor Y"},
    )
    r = client.get(f"{API}/books/")
    assert r.status_code == status.HTTP_200_OK
    books = r.json()
    assert len(books) == 2
    titulos = {b["titulo"] for b in books}
    assert titulos == {"Livro A", "Livro B"}


def test_filter_by_author(client):
    """
    Cria livros de diferentes autores
    e verifica se a filtragem por autor funciona corretamente.
    """
    client.post(
        f"{API}/books/",
        json={"titulo": "Obra 1", "autor": "Clarice Lispector"},
    )
    client.post(
        f"{API}/books/",
        json={"titulo": "Obra 2", "autor": "Machado de Assis"},
    )
    r = client.get(f"{API}/books/author", params={"author": "clarice"})
    assert r.status_code == status.HTTP_200_OK
    books = r.json()
    assert len(books) == 1
    assert books[0]["autor"] == "Clarice Lispector"


def test_filter_by_titulo(client):
    """
    Cria livros com títulos diferentes
    e verifica se a filtragem por título funciona corretamente.
    """
    client.post(
        f"{API}/books/",
        json={"titulo": "Memórias Póstumas", "autor": "Machado de Assis"},
    )
    client.post(
        f"{API}/books/",
        json={"titulo": "Dom Casmurro", "autor": "Machado de Assis"},
    )
    r = client.get(f"{API}/books/titulo", params={"titulo": "memórias"})
    assert r.status_code == status.HTTP_200_OK
    books = r.json()
    assert len(books) == 1
    assert books[0]["titulo"] == "Memórias Póstumas"


def test_filter_titulo_without_param_returns_all(client):
    """
    Verifica se a filtragem por título retorna todos os livros
    quando nenhum parâmetro é fornecido.
    """
    client.post(
        f"{API}/books/",
        json={"titulo": "A", "autor": "X"},
    )
    client.post(
        f"{API}/books/",
        json={"titulo": "B", "autor": "Y"},
    )
    r = client.get(f"{API}/books/titulo")
    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()) == 2
