FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /workspace

RUN pip install --no-cache-dir poetry

# Instala dependencias do hub
COPY streamlit_hub/pyproject.toml streamlit_hub/
RUN cd streamlit_hub && poetry install --only main

# Copia codigo
COPY streamlit_hub streamlit_hub

WORKDIR /workspace/streamlit_hub

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
