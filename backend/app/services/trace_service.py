from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.trace import Trace
from app.schemas.trace import TraceCreate


async def create_trace(
    db: AsyncSession,
    trace_data: TraceCreate,
) -> Trace:
    # Verify that the target project exists.
    result = await db.execute(
        select(Project).where(Project.id == trace_data.project_id)
    )
    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # Prevent duplicate trace IDs.
    result = await db.execute(
        select(Trace).where(Trace.trace_id == trace_data.trace_id)
    )
    existing_trace = result.scalar_one_or_none()

    if existing_trace is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Trace already exists",
        )

    trace = Trace(
        trace_id=trace_data.trace_id,
        project_id=trace_data.project_id,
        prompt_version_id=trace_data.prompt_version_id,
        provider=trace_data.provider,
        model=trace_data.model,
        input=trace_data.input,
        output=trace_data.output,
        input_tokens=trace_data.input_tokens,
        output_tokens=trace_data.output_tokens,
        total_tokens=trace_data.total_tokens,
        latency_ms=trace_data.latency_ms,
        estimated_cost=trace_data.estimated_cost,
        status=trace_data.status,
        error_message=trace_data.error_message,
        metadata_=trace_data.metadata,
    )

    db.add(trace)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Trace already exists",
        )

    await db.refresh(trace)

    return trace