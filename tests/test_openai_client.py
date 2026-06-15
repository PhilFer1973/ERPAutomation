import base64
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vision_agent.action_schema import VisionAnalysisRequest  # noqa: E402
from vision_agent.config import AgentConfig  # noqa: E402
from vision_agent.openai_client import (  # noqa: E402
    OpenAIClientError,
    analyse_with_openai,
    image_mime_type,
    screenshot_data_url,
)


VALID_RESPONSE = {
    "checkpoint_type": "NEW_VENDOR_SCREEN",
    "status": "continue",
    "screen_state": "new_vendor_screen_visible",
    "confidence": 0.93,
    "audit_comment": "The expected screen is visible.",
    "visible_errors": [],
    "extracted_reference": None,
}


class FakeResponse:
    output_text = json.dumps(VALID_RESPONSE)


class FakeResponsesClient:
    def __init__(self):
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return FakeResponse()


class FakeClient:
    def __init__(self):
        self.responses = FakeResponsesClient()


def test_screenshot_data_url_uses_supported_mime_type(tmp_path):
    image_path = tmp_path / "screen.png"
    image_path.write_bytes(b"fake-image-bytes")

    data_url = screenshot_data_url(image_path)

    assert data_url.startswith("data:image/png;base64,")
    assert data_url.endswith(base64.b64encode(b"fake-image-bytes").decode("ascii"))


def test_unsupported_screenshot_type_is_rejected(tmp_path):
    image_path = tmp_path / "screen.bmp"
    image_path.write_bytes(b"fake-image-bytes")

    with pytest.raises(OpenAIClientError):
        image_mime_type(image_path)


def test_analyse_with_openai_builds_responses_vision_payload(tmp_path):
    image_path = tmp_path / "screen.png"
    image_path.write_bytes(b"fake-image-bytes")
    request = VisionAnalysisRequest(
        run_id="RUN-004",
        supplier_request_id="42",
        checkpoint_type="NEW_VENDOR_SCREEN",
        screenshot_path=image_path,
        expected_screen="GnuCash New Vendor screen",
    )
    config = AgentConfig(
        openai_api_key="test-key",
        openai_model="gpt-4.1-mini",
        mock_mode=False,
    )
    client = FakeClient()

    result = analyse_with_openai(request, config, "Validate the screen.", client=client)

    assert result == VALID_RESPONSE
    call = client.responses.kwargs
    assert call["model"] == "gpt-4.1-mini"
    assert "Power Automate Desktop is the executor" in call["instructions"]
    assert call["text"]["format"]["type"] == "json_schema"
    assert call["text"]["format"]["strict"] is True
    assert call["input"][0]["content"][0]["type"] == "input_text"
    assert call["input"][0]["content"][1]["type"] == "input_image"
    assert call["input"][0]["content"][1]["image_url"].startswith("data:image/png;base64,")


def test_real_mode_requires_api_key_before_client_call(tmp_path):
    image_path = tmp_path / "screen.png"
    image_path.write_bytes(b"fake-image-bytes")
    request = VisionAnalysisRequest(
        run_id="RUN-005",
        supplier_request_id="42",
        checkpoint_type="NEW_VENDOR_SCREEN",
        screenshot_path=image_path,
        expected_screen="GnuCash New Vendor screen",
    )
    config = AgentConfig(openai_api_key=None, mock_mode=False)

    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        analyse_with_openai(request, config, "Validate the screen.", client=FakeClient())
