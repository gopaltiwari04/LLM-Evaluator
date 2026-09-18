from dataclasses import dataclass
from typing import Any


@dataclass
class TraceData:
    trace_id: str
    project_id: str
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
    metadata: dict[str, Any] | None = None