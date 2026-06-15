import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vision_agent.action_schema import (  # noqa: E402
    SchemaValidationError,
    VisionAnalysisRequest,
    apply_confidence_policy,
    validate_vision_response,
)


def test_valid_vision_response_is_normalized():
    response = validate_vision_response(
        {
            "checkpoint_type": "NEW_VENDOR_SCREEN",
            "status": "continue",
            "screen_state": "new_vendor_screen_visible",
            "confidence": 0.96,
            "audit_comment": "The expected screen is visible.",
            "visible_errors": [],
            "extracted_reference": None,
        },
        expected_checkpoint="NEW_VENDOR_SCREEN",
    )

    assert response["confidence"] == 0.96
    assert response["status"] == "continue"


def test_invalid_status_is_rejected():
    with pytest.raises(SchemaValidationError):
        validate_vision_response(
            {
                "checkpoint_type": "NEW_VENDOR_SCREEN",
                "status": "click_everything",
                "screen_state": "new_vendor_screen_visible",
                "confidence": 0.96,
                "audit_comment": "Bad status.",
                "visible_errors": [],
                "extracted_reference": None,
            }
        )


def test_low_confidence_changes_continue_to_review():
    adjusted = apply_confidence_policy(
        {
            "checkpoint_type": "FIELD_VALUE_CHECK",
            "status": "continue",
            "screen_state": "expected_field_value_visible",
            "confidence": 0.76,
            "audit_comment": "The field appears visible.",
            "visible_errors": [],
            "extracted_reference": None,
        },
        threshold=0.85,
    )

    assert adjusted["status"] == "stop_for_review"


def test_pad_request_schema_requires_supported_checkpoint():
    request = VisionAnalysisRequest.from_dict(
        {
            "run_id": "RUN-001",
            "supplier_request_id": "42",
            "checkpoint_type": "NEW_VENDOR_SCREEN",
            "screenshot_path": "screenshots/archive/RUN-001/step-002.png",
            "expected_screen": "GnuCash New Vendor screen",
            "supplier_context": {"supplier_legal_name": "Blue Kite Consulting Ltd"},
        }
    )

    assert request.checkpoint_type == "NEW_VENDOR_SCREEN"
    assert request.supplier_context["supplier_legal_name"] == "Blue Kite Consulting Ltd"
