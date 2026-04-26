from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Pergunta do usuario")


class AnswerResponse(BaseModel):
    answer: str


class IngestResponse(BaseModel):
    message: str
