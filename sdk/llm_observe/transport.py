import httpx

from .models import TraceData


class ObservatoryTransport:
    def __init__(
        self,
        api_key: str,
        endpoint: str,
    ) -> None:
        self.api_key = api_key
        self.endpoint = endpoint.rstrip("/")

    def send_trace(self, trace: TraceData) -> None:
        payload = {
            "trace_id": trace.trace_id,
            "project_id": trace.project_id,
            "prompt_version_id": None,
            "provider": trace.provider,
            "model": trace.model,
            "input": trace.input,
            "output": trace.output,
            "input_tokens": trace.input_tokens,
            "output_tokens": trace.output_tokens,
            "total_tokens": trace.total_tokens,
            "latency_ms": trace.latency_ms,
            "estimated_cost": trace.estimated_cost,
            "status": trace.status,
            "error_message": trace.error_message,
            "metadata": trace.metadata,
        }

        response = httpx.post(
            f"{self.endpoint}/api/v1/traces",
            headers={
                "X-API-Key": self.api_key,
            },
            json=payload,
            timeout=5.0,
        )

        response.raise_for_status()