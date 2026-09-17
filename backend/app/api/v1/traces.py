from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
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
) -> TraceResponse:
    trace = await create_trace(
        db=db,
        trace_data=trace_data,
    )

    return trace