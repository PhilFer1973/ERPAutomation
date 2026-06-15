"""Screen analysis orchestration for mock and future Vision-backed modes."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Union

from .action_schema import (
    VisionAnalysisRequest,
    apply_confidence_policy,
    validate_vision_response,
)
from .audit_logger import write_json_log
from .config import AgentConfig
from .openai_client import analyse_with_openai


MOCK_SCREEN_STATES = {
    "GN_CASH_MAIN_SCREEN": "gnucash_main_screen_visible",
    "NEW_VENDOR_SCREEN": "new_vendor_screen_visible",
    "FIELD_VALUE_CHECK": "expected_field_value_visible",
    "SAVE_CONFIRMATION": "vendor_save_confirmation_visible",
    "FINAL_RECORD_CHECK": "created_vendor_record_visible",
    "ERROR_SCREEN_CHECK": "no_visible_error_detected",
}


def build_checkpoint_prompt(request: VisionAnalysisRequest) -> str:
    """Build a compact checkpoint prompt for the future real Vision call."""

    parts = [
        "You are validating a desktop finance automation checkpoint.",
        f"Checkpoint type: {request.checkpoint_type}",
        f"Expected screen: {request.expected_screen}",
        "Return only strict JSON that matches schemas/vision_action.schema.json.",
    ]
    if request.expected_field:
        parts.append(f"Expected field: {request.expected_field}")
    if request.expected_value:
        parts.append(f"Expected value: {request.expected_value}")
    return "\n".join(parts)


def build_mock_response(request: VisionAnalysisRequest) -> Dict[str, Any]:
    """Return a valid fake Vision response for local development and tests."""

    status = "complete_success" if request.checkpoint_type == "SAVE_CONFIRMATION" else "continue"
    return {
        "checkpoint_type": request.checkpoint_type,
        "status": status,
        "screen_state": MOCK_SCREEN_STATES.get(request.checkpoint_type, "mock_screen_state"),
        "confidence": 0.96,
        "audit_comment": (
            f"Mock mode: assuming checkpoint {request.checkpoint_type} "
            f"matches {request.expected_screen}."
        ),
        "visible_errors": [],
        "extracted_reference": None,
    }


def analyse_screen(
    request: Union[VisionAnalysisRequest, Dict[str, Any]],
    config: AgentConfig | None = None,
) -> Dict[str, Any]:
    """Analyse a screen checkpoint and return normalized JSON for PAD."""

    config = config or AgentConfig.from_env()
    parsed_request = (
        request if isinstance(request, VisionAnalysisRequest) else VisionAnalysisRequest.from_dict(request)
    )

    if config.mock_mode:
        response = build_mock_response(parsed_request)
    else:
        prompt = build_checkpoint_prompt(parsed_request)
        response = analyse_with_openai(parsed_request, config, prompt)

    validated = validate_vision_response(response, expected_checkpoint=parsed_request.checkpoint_type)
    policy_checked = apply_confidence_policy(validated, threshold=config.confidence_threshold)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_name = f"vision-response-{parsed_request.checkpoint_type.lower()}-{stamp}.json"
    log_path = write_json_log(
        parsed_request.run_id,
        log_name,
        {"request": parsed_request.to_dict(), "response": policy_checked},
        config.log_root,
    )

    result = dict(policy_checked)
    result["raw_model_response_path"] = str(log_path)
    return result
