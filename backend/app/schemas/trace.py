from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TraceCreate(BaseModel):
    trace_id: str
    project_id: UUID
    prompt_version_id: UUID | None = None

    provider: str
    model: str

    input: str
    output: str | None = None

    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

    latency_ms: int | None = None
    estimated_cost: float | None = None

    status: str = "success"
    error_message: str | None = None

    metadata: dict | None = None


class TraceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    trace_id: str
    project_id: UUID
    prompt_version_id: UUID | None

    provider: str
    model: str

    input: str
    output: str | None

    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None

    latency_ms: int | None
    estimated_cost: float | None

    status: str
    error_message: str | None

    metadata: dict | None = Field(
        default=None,
        validation_alias="metadata_",
    )

    created_at: datetime


class TraceListResponse(BaseModel):
    items: list[TraceResponse]
    total: int
    limit: int
    offset: int