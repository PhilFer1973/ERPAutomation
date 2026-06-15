"""Local JSON audit logging for the Vision helper."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def safe_run_id(run_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", run_id.strip())
    return cleaned or "unknown-run"


def ensure_run_log_dir(run_id: str, log_root: Path) -> Path:
    run_dir = Path(log_root) / safe_run_id(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def write_json_log(
    run_id: str,
    file_name: str,
    payload: Dict[str, Any],
    log_root: Path = Path("logs"),
) -> Path:
    run_dir = ensure_run_log_dir(run_id, log_root)
    path = run_dir / file_name
    envelope = {
        "logged_at_utc": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    path.write_text(json.dumps(envelope, indent=2, sort_keys=True), encoding="utf-8")
    return path
