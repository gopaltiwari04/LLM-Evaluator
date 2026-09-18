import time
from typing import Any

from openai import OpenAI

from ..client import LLMObserver


GEMINI_BASE_URL = (
    "https://generativelanguage.googleapis.com/v1beta/openai/"
)


class ObservedGemini:
    """
    Gemini client with automatic LLM Observatory instrumentation.

    Uses Google's OpenAI-compatible Gemini API endpoint.
    """

    def __init__(
        self,
        observer: LLMObserver,
        api_key: str,
    ) -> None:
        self.observer = observer

        self.client = OpenAI(
            api_key=api_key,
            base_url=GEMINI_BASE_URL,
        )

    def chat_completion(
        self,
        *,
        project_id: str,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any,
    ):
        start = time.perf_counter()

        input_text = self._messages_to_text(messages)

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs,
            )

            latency_ms = int(
                (time.perf_counter() - start) * 1000
            )

            output_text = ""

            if response.choices:
                output_text = (
                    response.choices[0].message.content
                    or ""
                )

            usage = response.usage

            input_tokens = None
            output_tokens = None
            total_tokens = None

            if usage is not None:
                input_tokens = getattr(
                    usage,
                    "prompt_tokens",
                    None,
                )

                output_tokens = getattr(
                    usage,
                    "completion_tokens",
                    None,
                )

                total_tokens = getattr(
                    usage,
                    "total_tokens",
                    None,
                )

            estimated_cost = self._estimate_cost(
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )

            trace_id = self.observer.trace(
                project_id=project_id,
                provider="gemini",
                model=model,
                input=input_text,
                output=output_text,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                latency_ms=latency_ms,
                estimated_cost=estimated_cost,
                status="success",
                metadata={
                    "source": "gemini",
                    "instrumentation": "automatic",
                },
            )

            return response, trace_id

        except Exception as exc:
            latency_ms = int(
                (time.perf_counter() - start) * 1000
            )

            self.observer.trace(
                project_id=project_id,
                provider="gemini",
                model=model,
                input=input_text,
                output=None,
                latency_ms=latency_ms,
                estimated_cost=0.0,
                status="error",
                error_message=str(exc),
                metadata={
                    "source": "gemini",
                    "instrumentation": "automatic",
                    "error_type": type(exc).__name__,
                },
            )

            raise

    @staticmethod
    def _messages_to_text(
        messages: list[dict[str, Any]],
    ) -> str:
        parts: list[str] = []

        for message in messages:
            role = message.get("role", "unknown")
            content = message.get("content", "")

            parts.append(
                f"{role}: {content}"
            )

        return "\n".join(parts)

    @staticmethod
    def _estimate_cost(
        *,
        model: str,
        input_tokens: int | None,
        output_tokens: int | None,
    ) -> float:
        """
        Estimate theoretical paid-tier cost in USD.

        Gemini 2.5 Flash:
        input:  $0.30 / 1M tokens
        output: $2.50 / 1M tokens

        Development Free Tier usage itself may cost $0.
        """

        if input_tokens is None:
            input_tokens = 0

        if output_tokens is None:
            output_tokens = 0

        if model == "gemini-2.5-flash":
            input_cost = (
                input_tokens / 1_000_000
            ) * 0.30

            output_cost = (
                output_tokens / 1_000_000
            ) * 2.50

            return input_cost + output_cost

        return 0.0