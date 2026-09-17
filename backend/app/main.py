from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import AsyncSessionLocal


app = FastAPI(
    title="LLM Observatory API",
    description="LLM evaluation and observability platform",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "llm-observatory-api",
    }


@app.get("/health/db")
async def database_health():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar()

    return {
        "status": "ok",
        "database": value == 1,
    }