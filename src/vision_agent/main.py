"""Command-line entrypoint used by Power Automate Desktop."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from vision_agent.config import AgentConfig
    from vision_agent.screen_analyser import analyse_screen
else:
    from .config import AgentConfig
    from .screen_analyser import analyse_screen


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a screenshot checkpoint.")
    parser.add_argument("--input-json", required=True, help="Path to PAD checkpoint input JSON.")
    parser.add_argument("--output-json", required=False, help="Where to write helper output JSON.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    input_path = Path(args.input_json)
    # PAD commonly writes UTF-8 files with a BOM, so accept that transparently.
    payload = json.loads(input_path.read_text(encoding="utf-8-sig"))

    result = analyse_screen(payload, AgentConfig.from_env())

    if args.output_json:
        output_path = Path(args.output_json)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        print(str(output_path))
    else:
        print(json.dumps(result, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
