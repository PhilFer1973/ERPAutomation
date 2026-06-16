import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vision_agent.action_schema import CHECKPOINT_TYPES, VisionAnalysisRequest  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "sample-data" / "pad-checkpoints"
MANIFEST_PATH = ROOT / "pad" / "checkpoint-manifest.json"
PAD_SCHEMA_PATH = ROOT / "schemas" / "pad_checkpoint_request.schema.json"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_pad_checkpoint_samples_match_helper_contract():
    sample_paths = sorted(SAMPLE_DIR.glob("step-*.json"))

    assert len(sample_paths) == 8
    for sample_path in sample_paths:
        request = VisionAnalysisRequest.from_dict(_load_json(sample_path))
        assert request.checkpoint_type in CHECKPOINT_TYPES
        assert request.screenshot_path.as_posix().startswith("screenshots/archive/")


def test_pad_manifest_matches_sample_checkpoint_sequence():
    manifest = _load_json(MANIFEST_PATH)
    manifest_checkpoints = manifest["checkpoints"]
    sample_payloads = [_load_json(path) for path in sorted(SAMPLE_DIR.glob("step-*.json"))]

    assert len(manifest_checkpoints) == len(sample_payloads)
    assert [item["step_number"] for item in manifest_checkpoints] == list(range(1, 9))
    assert [item["checkpoint_type"] for item in manifest_checkpoints] == [
        item["checkpoint_type"] for item in sample_payloads
    ]
    assert [item["screenshot_file"] for item in manifest_checkpoints] == [
        Path(item["screenshot_path"]).name for item in sample_payloads
    ]


def test_pad_checkpoint_schema_enum_matches_helper_contract():
    schema = _load_json(PAD_SCHEMA_PATH)

    assert set(schema["properties"]["checkpoint_type"]["enum"]) == CHECKPOINT_TYPES
