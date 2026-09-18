from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trace import Trace


async def list_project_traces(
    db: AsyncSession,
    project_id: UUID,
    limit: int,
    offset: int,
) -> tuple[list[Trace], int]:

    count_result = await db.execute(
        select(func.count(Trace.id)).where(
            Trace.project_id == project_id
        )
    )

    total = count_result.scalar_one()

    result = await db.execute(
        select(Trace)
        .where(Trace.project_id == project_id)
        .order_by(Trace.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    traces = list(result.scalars().all())

    return traces, total