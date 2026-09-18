from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_api_key
from app.db.database import get_db
from app.models.api_key import APIKey
from app.schemas.trace import TraceCreate, TraceResponse
from app.services.trace_service import create_trace


router = APIRouter(
    prefix="/traces",
    tags=["traces"],
)


@router.post(
    "",
    response_model=TraceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def ingest_trace(
    trace_data: TraceCreate,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
) -> TraceResponse:
    # API keys are scoped to a single project.
    if trace_data.project_id != api_key.project_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key is not authorized for this project",
        )

    trace = await create_trace(
        db=db,
        trace_data=trace_data,
    )

    return trace