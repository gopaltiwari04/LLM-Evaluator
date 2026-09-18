from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_api_key
from app.db.database import get_db
from app.models.api_key import APIKey
from app.models.project import Project
from app.schemas.trace import TraceCreate
from app.workers.trace_tasks import store_trace


router = APIRouter(
    prefix="/traces",
    tags=["traces"],
)


@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED,
)
async def ingest_trace(
    trace_data: TraceCreate,
    db: AsyncSession = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
):
    # API keys are scoped to a single project.
    if trace_data.project_id != api_key.project_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key is not authorized for this project",
        )

    # Verify that the target project exists.
    result = await db.execute(
        select(Project).where(
            Project.id == trace_data.project_id
        )
    )

    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # Convert the Pydantic model into JSON-safe data.
    trace_payload = trace_data.model_dump(mode="json")

    # Queue persistence in Celery.
    task = store_trace.delay(trace_payload)

    return {
        "status": "accepted",
        "trace_id": trace_data.trace_id,
        "task_id": task.id,
    }