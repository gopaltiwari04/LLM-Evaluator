import asyncio

from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.models.trace import Trace
from app.workers.celery_app import celery_app


async def _store_trace(trace_data: dict) -> None:
    async with AsyncSessionLocal() as db:
        # Protect against duplicate trace IDs.
        result = await db.execute(
            select(Trace).where(
                Trace.trace_id == trace_data["trace_id"]
            )
        )

        if result.scalar_one_or_none() is not None:
            return

        trace = Trace(
            trace_id=trace_data["trace_id"],
            project_id=trace_data["project_id"],
            prompt_version_id=trace_data.get("prompt_version_id"),
            provider=trace_data["provider"],
            model=trace_data["model"],
            input=trace_data["input"],
            output=trace_data.get("output"),
            input_tokens=trace_data.get("input_tokens"),
            output_tokens=trace_data.get("output_tokens"),
            total_tokens=trace_data.get("total_tokens"),
            latency_ms=trace_data.get("latency_ms"),
            estimated_cost=trace_data.get("estimated_cost"),
            status=trace_data.get("status", "success"),
            error_message=trace_data.get("error_message"),
            metadata_=trace_data.get("metadata"),
        )

        db.add(trace)
        await db.commit()


@celery_app.task(
    name="store_trace",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def store_trace(trace_data: dict) -> None:
    asyncio.run(_store_trace(trace_data))