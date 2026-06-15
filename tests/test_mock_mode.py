import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vision_agent import AgentConfig, VisionAnalysisRequest, build_mock_response  # noqa: E402
from vision_agent.action_schema import validate_vision_response  # noqa: E402


def test_mock_mode_defaults_to_enabled():
    config = AgentConfig.from_env(env_file=None)

    assert config.mock_mode is True
    assert config.confidence_threshold == 0.85


def test_mock_response_matches_schema():
    request = VisionAnalysisRequest(
        run_id="RUN-003",
        supplier_request_id="42",
        checkpoint_type="GN_CASH_MAIN_SCREEN",
        screenshot_path=Path("screenshots/archive/RUN-003/step-001.png"),
        expected_screen="GnuCash main screen",
    )

    response = build_mock_response(request)
    validated = validate_vision_response(response, expected_checkpoint="GN_CASH_MAIN_SCREEN")

    assert validated["status"] == "continue"
    assert validated["visible_errors"] == []
