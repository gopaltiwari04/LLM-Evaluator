from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_api_key
from app.db.database import get_db
from app.models.api_key import APIKey
from app.models.project import Project
from app.schemas.trace import TraceListResponse, TraceResponse
from app.services.trace_query_service import list_project_traces


router = APIRouter(
    prefix="/projects",
    tags=["traces"],
)


@router.get(
    "/{project_id}/traces",
    response_model=TraceListResponse,
)
async def get_project_traces(
    project_id: UUID,
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
) -> TraceListResponse:

    if project_id != api_key.project_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key is not authorized for this project",
        )

    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )

    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    traces, total = await list_project_traces(
        db=db,
        project_id=project_id,
        limit=limit,
        offset=offset,
    )

    return TraceListResponse(
        items=[
            TraceResponse.model_validate(trace)
            for trace in traces
        ],
        total=total,
        limit=limit,
        offset=offset,
    )