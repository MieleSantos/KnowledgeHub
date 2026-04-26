from fastapi import APIRouter, Header, HTTPException, status

from app.integrations.ai_backend import (
    ask_chatbot,
    ask_semantic_search,
    ingest_semantic_documents,
)
from app.schemas.ai_schemas import AnswerResponse, IngestResponse, QuestionRequest

router = APIRouter()


@router.post(
    "/chatbot/ask", response_model=AnswerResponse, status_code=status.HTTP_200_OK
)
async def chatbot_ask(
    payload: QuestionRequest,
    x_openai_key: str | None = Header(None, alias="X-OpenAI-Key"),
) -> AnswerResponse:
    try:
        answer = ask_chatbot(payload.question, api_key=x_openai_key)
        return AnswerResponse(answer=answer)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post(
    "/semantic-search/ingest",
    response_model=IngestResponse,
    status_code=status.HTTP_200_OK,
)
async def semantic_ingest() -> IngestResponse:
    try:
        message = ingest_semantic_documents()
        return IngestResponse(message=message or "Ingestao concluida.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post(
    "/semantic-search/ask",
    response_model=AnswerResponse,
    status_code=status.HTTP_200_OK,
)
async def semantic_ask(
    payload: QuestionRequest,
    x_openai_key: str | None = Header(None, alias="X-OpenAI-Key"),
) -> AnswerResponse:
    try:
        answer = ask_semantic_search(payload.question, api_key=x_openai_key)
        return AnswerResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
