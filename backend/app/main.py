from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.organizations import router as organizations_router
from app.api.v1.projects import router as projects_router

from app.api.v1.traces import router as traces_router
from app.api.v1.api_keys import router as api_keys_router
from app.db.database import AsyncSessionLocal
from app.api.v1.project_traces import router as project_traces_router
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.openapi.utils import get_openapi
from fastapi.security import APIKeyHeader


app = FastAPI(
    title="LLM Observatory API",
    description="LLM evaluation and observability platform",
    version="0.1.0",
)


app.include_router(
    traces_router,
    prefix="/api/v1",
)
app.include_router(
    organizations_router,
    prefix="/api/v1",
)

app.include_router(
    projects_router,
    prefix="/api/v1",
)
app.include_router(
    api_keys_router,
    prefix="/api/v1",
)
app.include_router(
    project_traces_router,
    prefix="/api/v1",
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