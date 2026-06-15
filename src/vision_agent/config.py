"""Configuration loading for the Vision helper."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - allows tests before dependencies are installed
    load_dotenv = None


def _parse_bool(value: Optional[str], default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _parse_float(value: Optional[str], default: float) -> float:
    if value is None or value.strip() == "":
        return default
    parsed = float(value)
    if parsed < 0 or parsed > 1:
        raise ValueError("CONFIDENCE_THRESHOLD must be between 0 and 1.")
    return parsed


@dataclass(frozen=True)
class AgentConfig:
    """Runtime settings for mock or Vision-backed analysis."""

    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4.1-mini"
    mock_mode: bool = True
    confidence_threshold: float = 0.85
    log_root: Path = Path("logs")
    screenshot_root: Path = Path("screenshots")

    @classmethod
    def from_env(cls, env_file: Optional[str] = ".env") -> "AgentConfig":
        if env_file and load_dotenv is not None and Path(env_file).exists():
            load_dotenv(env_file)

        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            mock_mode=_parse_bool(os.getenv("MOCK_MODE"), True),
            confidence_threshold=_parse_float(os.getenv("CONFIDENCE_THRESHOLD"), 0.85),
            log_root=Path(os.getenv("LOG_ROOT", "logs")),
            screenshot_root=Path(os.getenv("SCREENSHOT_ROOT", "screenshots")),
        )

    def require_real_vision_ready(self) -> None:
        if self.mock_mode:
            return
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when MOCK_MODE is false.")
