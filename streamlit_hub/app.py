"""Frontend Streamlit para Library Book API."""

import os

import requests
import streamlit as st


def get_api_base_url() -> str:
    return os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


def get_openai_key() -> str | None:
    return st.session_state.get("openai_key")


def check_api_health() -> bool:
    ok, _, _ = api_get("/api/v1/health")
    return ok


def api_get(path: str, params: dict | None = None) -> tuple[bool, str, object]:
    try:
        response = requests.get(f"{get_api_base_url()}{path}", params=params, timeout=20)
        response.raise_for_status()
        return True, "", response.json()
    except requests.RequestException as exc:
        return False, str(exc), {}


def api_post(path: str, payload: dict | None = None) -> tuple[bool, str, object]:
    try:
        headers = {}
        openai_key = get_openai_key()
        if openai_key:
            headers["X-OpenAI-Key"] = openai_key

        response = requests.post(
            f"{get_api_base_url()}{path}",
            json=payload or {},
            headers=headers,
            timeout=120,
        )
        response.raise_for_status()
        return True, "", response.json()
    except requests.RequestException as exc:
        return False, str(exc), {}


def render_header(api_ok: bool) -> None:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### 📚 Library Book")
        st.caption("Sistema de Gerenciamento de Biblioteca com IA")
    with col2:
        if api_ok:
            st.success("🟢 API Online")
        else:
            st.error("🔴 API Offline")


def render_books_page() -> None:
    st.header("📚 Biblioteca de Livros")
    st.markdown("Gerencie seu catálogo de livros")
    st.divider()

    col_search, col_add = st.columns([3, 1])
    with col_search:
        st.subheader("🔍 Buscar Livros")
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            search_query = st.text_input("Buscar...", placeholder="Título ou autor...", label_visibility="collapsed")
        with col2:
            page = st.number_input("Página", min_value=1, value=1, step=1, label_visibility="collapsed")
        with col3:
            size = st.selectbox("Itens", [5, 10, 20, 50], index=1, label_visibility="collapsed")

        params = {"page": page, "size": size}
        if search_query:
            params["q"] = search_query

        ok, error, data = api_get("/api/v1/books/", params)

        if ok:
            items = data.get("items", [])
            total = data.get("total", 0)
            pages = data.get("pages", 1)
            current_page = data.get("page", 1)
            st.caption(f"📊 {total} livro(s) | Página {current_page}/{pages}")

            if not items:
                st.info("Nenhum livro encontrado.")
            else:
                for book in items:
                    with st.container():
                        col_left, col_right = st.columns([4, 1])
                        with col_left:
                            st.markdown(f"**{book.get('titulo', 'Sem título')}**")
                            st.caption(f"👤 {book.get('autor', 'Desconhecido')}")
                            if book.get("resumo"):
                                st.caption(f"_{book.get('resumo')}_")
                        with col_right:
                            if book.get("data_publicacao"):
                                st.caption(f"📅 {book.get('data_publicacao')}")
                        st.divider()
        else:
            st.error(f"Erro: {error}")

    with col_add:
        st.subheader("➕ Novo Livro")
        with st.form("create_book_form", clear_on_submit=True):
            titulo = st.text_input("Título", placeholder="Ex: Dom Casmurro")
            autor = st.text_input("Autor", placeholder="Ex: Machado de Assis")
            data_publicacao = st.date_input("Data de Publicação", label_visibility="collapsed")
            resumo = st.text_area("Resumo", placeholder="Breve descrição...", height=80)
            submitted = st.form_submit_button("📖 Salvar", use_container_width=True)

            if submitted:
                if not titulo or not autor:
                    st.warning("Título e Autor são obrigatórios.")
                else:
                    payload = {
                        "titulo": titulo,
                        "autor": autor,
                        "data_publicacao": data_publicacao.isoformat() if data_publicacao else None,
                        "resumo": resumo or None,
                    }
                    ok, error, data = api_post("/api/v1/books/", payload)
                    if ok:
                        st.success(f"✅ '{data.get('titulo')}' criado!")
                    else:
                        st.error(f"Erro: {error}")


def render_chatbot_page() -> None:
    st.header("🤖 Assistente Python")

    st.markdown(
        "Tire suas dúvidas sobre Python! O assistente responde com base em boas práticas."
    )
    st.divider()

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    col_left, col_right = st.columns([3, 1])

    with col_left:
        if st.session_state.chat_messages:
            for role, content in st.session_state.chat_messages:
                with st.chat_message(role):
                    st.markdown(content)

    with col_right:
        st.markdown("### 💡 Exemplos")
        st.caption("Copie e cole no chat:")
        examples = [
            "Como usar list comprehension?",
            "O que são generators em Python?",
            "Explique decoradores",
            "Como tratar erros com try/except?",
        ]
        for ex in examples:
            st.code(ex, language=None)

    st.divider()
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        user_text = st.chat_input("Digite sua dúvida sobre Python...")
    with col_btn:
        st.write("")
        clear_clicked = st.button("🗑️", use_container_width=True)

    if clear_clicked:
        st.session_state.chat_messages = []
        st.rerun()

    if user_text:
        st.session_state.chat_messages.append(("user", user_text))

        with st.spinner("Pensando..."):
            ok, error, data = api_post("/api/v1/chatbot/ask", {"question": user_text})
            if ok:
                output = data.get("answer", "")
                st.session_state.chat_messages.append(("assistant", output))
            else:
                st.error(error)
        st.rerun()


def render_semantic_page() -> None:
    st.header("🔎 Busca Semântica (RAG)")

    st.markdown(
        "Faça perguntas sobre os documentos carregados. "
        "A resposta é gerada com base no conteúdo indexado."
    )
    st.divider()

    col_left, col_right = st.columns([3, 1])

    with col_right:
        st.markdown("### ⚙️ Configurações")
        if st.button("📥 Carregar Documentos", use_container_width=True):
            with st.spinner("Carregando documentos..."):
                ok, error, data = api_post("/api/v1/semantic-search/ingest")
                if ok:
                    st.success("✅ Documentos carregados com sucesso!")
                else:
                    st.error(f"Erro: {error}")

        st.markdown("### 💡 Sugestões")
        suggestions = [
            "O que são embeddings?",
            "Como funciona vector store?",
            "Explique LangChain",
            "O que é RAG?",
        ]
        for sug in suggestions:
            st.code(sug, language=None)

    with col_left:
        if "semantic_history" not in st.session_state:
            st.session_state.semantic_history = []

        question = st.text_input(
            "Digite sua pergunta:",
            placeholder="Ex: O que são embeddings?",
            key="question_input",
        )

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            ask_clicked = st.button("🔍 Perguntar", type="primary", use_container_width=True)
        with col_b2:
            clear_clicked = st.button("🗑️ Limpar", use_container_width=True)

        if clear_clicked:
            st.session_state.semantic_history = []
            st.rerun()

        if ask_clicked and question.strip():
            with st.spinner("Buscando resposta..."):
                ok, error, data = api_post("/api/v1/semantic-search/ask", {"question": question})
                st.session_state.semantic_history.append(
                    {"question": question, "ok": ok, "data": data, "error": error}
                )

        if st.session_state.semantic_history:
            st.markdown("### 📝 Histórico")
            for item in reversed(st.session_state.semantic_history[-5:]):
                with st.container():
                    st.markdown(f"**Pergunta:** {item['question']}")
                    if item["ok"]:
                        st.success(item["data"].get("answer", ""))
                    else:
                        st.error(f"Erro: {item['error']}")
                    st.divider()


def render_sidebar() -> str | None:
    with st.sidebar:
        st.markdown("### 🔑 OpenAI Key")
        with st.expander("Configurações"):
            openai_key = st.text_input(
                "API Key",
                type="password",
                placeholder="sk-...",
                help="Cole sua OpenAI API Key para usar IA",
            )
            if openai_key:
                st.session_state.openai_key = openai_key
            st.markdown("---")
        st.markdown("### 📚 Menu")
        page = st.radio(
            "Navegação",
            options=["📚 Livros", "🤖 Chatbot", "🔎 Busca Semântica"],
            label_visibility="visible",
        )
        return page


def main() -> None:
    st.set_page_config(
        page_title="Library Book",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    api_ok = check_api_health()
    render_header(api_ok)
    st.divider()

    page = render_sidebar()

    if page == "📚 Livros":
        render_books_page()
    elif page == "🤖 Chatbot":
        render_chatbot_page()
    else:
        render_semantic_page()


if __name__ == "__main__":
    main()
