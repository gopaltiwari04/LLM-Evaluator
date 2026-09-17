from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trace import Trace
from app.schemas.trace import TraceCreate


async def create_trace(
    db: AsyncSession,
    trace_data: TraceCreate,
) -> Trace:
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

    await db.commit()
    await db.refresh(trace)

    return trace