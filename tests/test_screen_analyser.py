import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vision_agent import AgentConfig, VisionAnalysisRequest, analyse_screen  # noqa: E402


def test_analyse_screen_returns_valid_mock_response_and_log(tmp_path):
    request = VisionAnalysisRequest(
        run_id="RUN-001",
        supplier_request_id="42",
        checkpoint_type="NEW_VENDOR_SCREEN",
        screenshot_path=Path("screenshots/archive/RUN-001/step-002.png"),
        expected_screen="GnuCash New Vendor screen",
        supplier_context={"supplier_legal_name": "Blue Kite Consulting Ltd"},
    )
    config = AgentConfig(mock_mode=True, log_root=tmp_path / "logs")

    result = analyse_screen(request, config)

    assert result["status"] == "continue"
    assert result["checkpoint_type"] == "NEW_VENDOR_SCREEN"
    assert result["confidence"] >= config.confidence_threshold

    log_path = Path(result["raw_model_response_path"])
    assert log_path.exists()
    logged = json.loads(log_path.read_text(encoding="utf-8"))
    assert logged["payload"]["request"]["run_id"] == "RUN-001"


def test_save_confirmation_mock_returns_complete_success(tmp_path):
    request = {
        "run_id": "RUN-002",
        "supplier_request_id": "42",
        "checkpoint_type": "SAVE_CONFIRMATION",
        "screenshot_path": "screenshots/archive/RUN-002/step-004.png",
        "expected_screen": "GnuCash save confirmation",
    }
    config = AgentConfig(mock_mode=True, log_root=tmp_path / "logs")

    result = analyse_screen(request, config)

    assert result["status"] == "complete_success"
