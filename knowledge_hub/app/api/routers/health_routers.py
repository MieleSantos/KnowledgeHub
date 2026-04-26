from __future__ import annotations

import os
from pathlib import Path

from fastapi import APIRouter, status

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def healthcheck() -> dict:
    root_dir = Path(__file__).resolve().parents[4]
    vectorstore_path = root_dir / "semantic_search" / "vectorstore"

    return {
        "status": "ok",
        "api": "up",
        "openai_key_configured": bool(os.getenv("OPENAI_API_KEY")),
        "vectorstore_exists": vectorstore_path.exists(),
        "vectorstore_path": str(vectorstore_path),
    }
