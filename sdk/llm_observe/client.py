import uuid

from .models import TraceData
from .transport import ObservatoryTransport


class LLMObserver:
    def __init__(
        self,
        api_key: str,
        endpoint: str = "http://127.0.0.1:8000",
    ) -> None:
        self.transport = ObservatoryTransport(
            api_key=api_key,
            endpoint=endpoint,
        )

    def trace(
        self,
        *,
        project_id: str,
        provider: str,
        model: str,
        input: str,
        output: str | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        total_tokens: int | None = None,
        latency_ms: int | None = None,
        estimated_cost: float | None = None,
        status: str = "success",
        error_message: str | None = None,
        metadata: dict | None = None,
    ) -> str:
        trace_id = f"trc_{uuid.uuid4().hex}"

        trace = TraceData(
            trace_id=trace_id,
            project_id=project_id,
            provider=provider,
            model=model,
            input=input,
            output=output,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            latency_ms=latency_ms,
            estimated_cost=estimated_cost,
            status=status,
            error_message=error_message,
            metadata=metadata,
        )

        self.transport.send_trace(trace)

        return trace_id