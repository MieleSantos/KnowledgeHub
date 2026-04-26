from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import ai_routers, book_routers, health_routers
from app.core.config import settings
from app.core.database import engine
from app.models.book_model import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="1.0.0",
    description="API para gerenciamento de um catálogo de livros",
)


app.include_router(book_routers.router, prefix="/api/v1")
app.include_router(ai_routers.router, prefix="/api/v1")
app.include_router(health_routers.router, prefix="/api/v1")
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
