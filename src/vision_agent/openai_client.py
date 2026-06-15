"""OpenAI Vision client boundary."""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any, Dict, Optional

from .action_schema import VISION_RESPONSE_JSON_SCHEMA, VisionAnalysisRequest
from .config import AgentConfig


class OpenAIClientError(RuntimeError):
    """Raised when the real Vision path cannot complete safely."""


MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}

SYSTEM_INSTRUCTIONS = (
    "You are validating screenshots from a controlled finance desktop automation. "
    "Power Automate Desktop is the executor. Inspect the screenshot, verify only "
    "the requested checkpoint, identify visible errors, and return strict JSON. "
    "Do not recommend unrestricted desktop control or approve supplier data."
)


def encode_screenshot(path: Path) -> str:
    """Return a base64 representation of a screenshot."""

    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


def image_mime_type(path: Path) -> str:
    """Infer the image MIME type expected by the OpenAI Vision API."""

    suffix = Path(path).suffix.lower()
    if suffix not in MIME_TYPES:
        supported = ", ".join(sorted(MIME_TYPES))
        raise OpenAIClientError(f"Unsupported screenshot type '{suffix}'. Supported: {supported}.")
    return MIME_TYPES[suffix]


def screenshot_data_url(path: Path) -> str:
    """Build a data URL for the screenshot, suitable for input_image."""

    screenshot_path = Path(path)
    if not screenshot_path.exists():
        raise FileNotFoundError(f"Screenshot not found: {screenshot_path}")
    return f"data:{image_mime_type(screenshot_path)};base64,{encode_screenshot(screenshot_path)}"


def _load_openai_client(config: AgentConfig) -> Any:
    try:
        from openai import OpenAI
    except ImportError as exc:  # pragma: no cover - exercised only without dependency installed
        raise OpenAIClientError("The 'openai' package is required when MOCK_MODE=false.") from exc

    return OpenAI(api_key=config.openai_api_key)


def _extract_text_from_response(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text

    if hasattr(response, "model_dump"):
        payload = response.model_dump()
    elif isinstance(response, dict):
        payload = response
    else:
        payload = {}

    for output_item in payload.get("output", []):
        for content_part in output_item.get("content", []):
            text = content_part.get("text")
            if isinstance(text, str) and text.strip():
                return text

    raise OpenAIClientError("OpenAI response did not contain output text.")


def _parse_response_json(response: Any) -> Dict[str, Any]:
    parsed = getattr(response, "output_parsed", None)
    if isinstance(parsed, dict):
        return parsed
    if hasattr(parsed, "model_dump"):
        return parsed.model_dump()

    output_text = _extract_text_from_response(response)
    try:
        parsed_json = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise OpenAIClientError("OpenAI response was not valid JSON.") from exc
    if not isinstance(parsed_json, dict):
        raise OpenAIClientError("OpenAI response JSON must be an object.")
    return parsed_json


def analyse_with_openai(
    request: VisionAnalysisRequest,
    config: AgentConfig,
    prompt: str,
    client: Optional[Any] = None,
) -> Dict[str, Any]:
    """Call OpenAI Vision using the Responses API and return parsed JSON."""

    config.require_real_vision_ready()
    active_client = client or _load_openai_client(config)

    response = active_client.responses.create(
        model=config.openai_model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": screenshot_data_url(request.screenshot_path),
                    },
                ],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "vision_checkpoint_response",
                "strict": True,
                "schema": VISION_RESPONSE_JSON_SCHEMA,
            }
        },
    )
    return _parse_response_json(response)
