"""OpenAI Vision client boundary.

Real Vision calls are intentionally left for Phase 2. V1 foundation work runs in
mock mode so tests and PAD handoff design do not require credentials or network.
"""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, Dict

from .action_schema import VisionAnalysisRequest
from .config import AgentConfig


class RealVisionNotImplementedError(RuntimeError):
    """Raised when real Vision mode is requested during the foundation phase."""


def encode_screenshot(path: Path) -> str:
    """Return a base64 representation of a screenshot for a future Vision call."""

    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


def analyse_with_openai(
    request: VisionAnalysisRequest,
    config: AgentConfig,
    prompt: str,
) -> Dict[str, Any]:
    """Placeholder for the Phase 2 OpenAI Vision implementation."""

    config.require_real_vision_ready()
    raise RealVisionNotImplementedError(
        "Real OpenAI Vision calls are reserved for Phase 2. Set MOCK_MODE=true for V1."
    )
