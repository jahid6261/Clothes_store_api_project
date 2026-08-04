from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.schema import AIRequestSchema
from src.ai.service import chat_service
from src.utils.db import get_db

ai_router = APIRouter(prefix="/ai", tags=["AI"])


@ai_router.post("/chat")
async def chat(request: AIRequestSchema, db: AsyncSession = Depends(get_db)):

    return await chat_service(
        db=db,
        question=request.prompt,
    )