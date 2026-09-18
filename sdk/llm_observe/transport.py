from concurrent.futures import ThreadPoolExecutor
from typing import Callable

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

        self._executor = ThreadPoolExecutor(
            max_workers=2,
            thread_name_prefix="llm-observatory",
        )

    def send_trace(self, trace: TraceData) -> None:
        """
        Send telemetry synchronously.

        This remains available for explicit synchronous use/testing.
        """
        self._post_trace(trace)

    def send_trace_async(
        self,
        trace: TraceData,
    ) -> None:
        """
        Submit telemetry in the background.

        The customer's application does not wait for the
        Observatory API request to complete.
        """
        self._executor.submit(
            self._safe_post_trace,
            trace,
        )

    def _safe_post_trace(
        self,
        trace: TraceData,
    ) -> None:
        try:
            self._post_trace(trace)
        except Exception:
            # Observability must never crash the customer's application.
            pass

    def _post_trace(
        self,
        trace: TraceData,
    ) -> None:
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

    def shutdown(self) -> None:
        """
        Gracefully stop the SDK background executor.
        """
        self._executor.shutdown(wait=True)