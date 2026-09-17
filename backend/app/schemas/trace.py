from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TraceCreate(BaseModel):
    trace_id: str = Field(min_length=1, max_length=100)
    project_id: UUID
    prompt_version_id: UUID | None = None

    provider: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=255)

    input: str
    output: str | None = None

    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)

    latency_ms: int | None = Field(default=None, ge=0)
    estimated_cost: float | None = Field(default=None, ge=0)

    status: str = Field(default="success", max_length=50)
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

    metadata: dict | None
    created_at: datetime