"""Validation helpers for PAD requests and Vision responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


ALLOWED_STATUSES = {
    "continue",
    "stop_for_review",
    "failed",
    "complete_success",
}

CHECKPOINT_TYPES = {
    "GN_CASH_MAIN_SCREEN",
    "NEW_VENDOR_SCREEN",
    "FIELD_VALUE_CHECK",
    "SAVE_CONFIRMATION",
    "FINAL_RECORD_CHECK",
    "ERROR_SCREEN_CHECK",
}

REQUIRED_VISION_FIELDS = {
    "checkpoint_type",
    "status",
    "screen_state",
    "confidence",
    "audit_comment",
    "visible_errors",
    "extracted_reference",
}

VISION_RESPONSE_JSON_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "checkpoint_type",
        "status",
        "screen_state",
        "confidence",
        "audit_comment",
        "visible_errors",
        "extracted_reference",
    ],
    "properties": {
        "checkpoint_type": {
            "type": "string",
            "enum": sorted(CHECKPOINT_TYPES),
            "description": "The checkpoint type supplied by Power Automate Desktop.",
        },
        "status": {
            "type": "string",
            "enum": sorted(ALLOWED_STATUSES),
            "description": "Whether PAD should continue, stop, fail, or mark successful completion.",
        },
        "screen_state": {
            "type": "string",
            "description": "Short machine-readable description of the visible screen state.",
        },
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Model confidence from 0 to 1.",
        },
        "audit_comment": {
            "type": "string",
            "description": "Short audit-friendly explanation of the result.",
        },
        "visible_errors": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Visible error or warning messages found in the screenshot.",
        },
        "extracted_reference": {
            "type": ["string", "null"],
            "description": "Visible supplier/vendor reference if present.",
        },
    },
}


class SchemaValidationError(ValueError):
    """Raised when request or response JSON does not match the V1 contract."""


def _require_string(payload: Dict[str, Any], field_name: str) -> str:
    value = payload.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise SchemaValidationError(f"{field_name} must be a non-empty string.")
    return value


def _missing_fields(payload: Dict[str, Any], fields: Iterable[str]) -> list[str]:
    return sorted(field for field in fields if field not in payload)


@dataclass(frozen=True)
class VisionAnalysisRequest:
    """Structured checkpoint request passed from PAD to the helper."""

    run_id: str
    supplier_request_id: str
    checkpoint_type: str
    screenshot_path: Path
    expected_screen: str
    expected_field: Optional[str] = None
    expected_value: Optional[str] = None
    supplier_context: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "VisionAnalysisRequest":
        missing = _missing_fields(
            payload,
            {
                "run_id",
                "supplier_request_id",
                "checkpoint_type",
                "screenshot_path",
                "expected_screen",
            },
        )
        if missing:
            raise SchemaValidationError(f"Missing request fields: {', '.join(missing)}")

        checkpoint_type = _require_string(payload, "checkpoint_type")
        if checkpoint_type not in CHECKPOINT_TYPES:
            raise SchemaValidationError(f"Unsupported checkpoint_type: {checkpoint_type}")

        supplier_context = payload.get("supplier_context") or {}
        if not isinstance(supplier_context, dict):
            raise SchemaValidationError("supplier_context must be an object when provided.")

        return cls(
            run_id=_require_string(payload, "run_id"),
            supplier_request_id=str(payload["supplier_request_id"]),
            checkpoint_type=checkpoint_type,
            screenshot_path=Path(_require_string(payload, "screenshot_path")),
            expected_screen=_require_string(payload, "expected_screen"),
            expected_field=payload.get("expected_field"),
            expected_value=payload.get("expected_value"),
            supplier_context=supplier_context,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "supplier_request_id": self.supplier_request_id,
            "checkpoint_type": self.checkpoint_type,
            "screenshot_path": str(self.screenshot_path),
            "expected_screen": self.expected_screen,
            "expected_field": self.expected_field,
            "expected_value": self.expected_value,
            "supplier_context": self.supplier_context,
        }


def validate_vision_response(
    payload: Dict[str, Any],
    expected_checkpoint: Optional[str] = None,
) -> Dict[str, Any]:
    """Validate and return a normalized Vision response payload."""

    if not isinstance(payload, dict):
        raise SchemaValidationError("Vision response must be a JSON object.")

    missing = _missing_fields(payload, REQUIRED_VISION_FIELDS)
    if missing:
        raise SchemaValidationError(f"Missing Vision response fields: {', '.join(missing)}")

    checkpoint_type = _require_string(payload, "checkpoint_type")
    if checkpoint_type not in CHECKPOINT_TYPES:
        raise SchemaValidationError(f"Unsupported checkpoint_type: {checkpoint_type}")
    if expected_checkpoint and checkpoint_type != expected_checkpoint:
        raise SchemaValidationError(
            f"Response checkpoint_type {checkpoint_type} does not match {expected_checkpoint}."
        )

    status = _require_string(payload, "status")
    if status not in ALLOWED_STATUSES:
        raise SchemaValidationError(f"Unsupported status: {status}")

    _require_string(payload, "screen_state")
    _require_string(payload, "audit_comment")

    confidence = payload.get("confidence")
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise SchemaValidationError("confidence must be a number between 0 and 1.")
    if confidence < 0 or confidence > 1:
        raise SchemaValidationError("confidence must be between 0 and 1.")

    visible_errors = payload.get("visible_errors")
    if not isinstance(visible_errors, list):
        raise SchemaValidationError("visible_errors must be an array.")
    if not all(isinstance(item, str) for item in visible_errors):
        raise SchemaValidationError("visible_errors must contain strings only.")

    extracted_reference = payload.get("extracted_reference")
    if extracted_reference is not None and not isinstance(extracted_reference, str):
        raise SchemaValidationError("extracted_reference must be a string or null.")

    normalized = dict(payload)
    normalized["confidence"] = float(confidence)
    return normalized


def apply_confidence_policy(
    response: Dict[str, Any],
    threshold: float = 0.85,
    review_floor: float = 0.70,
) -> Dict[str, Any]:
    """Apply the V1 stop-first confidence policy to a valid response."""

    normalized = validate_vision_response(response)
    confidence = normalized["confidence"]
    status = normalized["status"]

    if status not in {"continue", "complete_success"}:
        return normalized
    if confidence >= threshold:
        return normalized

    adjusted = dict(normalized)
    if confidence >= review_floor:
        adjusted["status"] = "stop_for_review"
        reason = "Confidence is below the configured threshold."
    else:
        adjusted["status"] = "failed"
        reason = "Confidence is below the V1 minimum review floor."

    adjusted["audit_comment"] = f"{normalized['audit_comment']} {reason}"
    return adjusted
