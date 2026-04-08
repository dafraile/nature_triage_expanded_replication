#!/usr/bin/env python3
"""Build a paper-original dataset with benchmark artifacts stripped out."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


WORKSPACE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = WORKSPACE_DIR / "data" / "canonical_singleturn_vignettes.json"
DEFAULT_V3_INPUT = WORKSPACE_DIR / "data" / "canonical_narrative_prompt_a_v3_vignettes.json"
DEFAULT_OUTPUT = WORKSPACE_DIR / "data" / "canonical_source_stripped_vignettes.json"

ARTIFACT_LINES = (
    "Please base your answer only on the information in this message.",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a canonical dataset using paper wording with benchmark artifacts removed",
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Canonical single-turn JSON")
    parser.add_argument(
        "--prompt-a-v3-input",
        type=Path,
        default=DEFAULT_V3_INPUT,
        help="Canonical Prompt A v3 JSON used to recover the shared scaffold prefix",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output JSON path")
    return parser.parse_args()


def normalize_blank_lines(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.strip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def strip_benchmark_artifacts(prompt: str) -> str:
    text = prompt.replace("\r\n", "\n").replace("\r", "\n")
    for line in ARTIFACT_LINES:
        text = text.replace(line, "")
    marker = re.search(r"\n\s*Please answer in exactly this format:\s*\n", text, flags=re.IGNORECASE)
    if marker:
        text = text[:marker.start()]
    return normalize_blank_lines(text)


def extract_prompt_a_prefix(v3_rows: list[dict]) -> str:
    for row in v3_rows:
        field = row.get("narrative_prompt_a", "")
        marker = "\n\nPatient message:\n"
        if marker in field:
            return field.split(marker, 1)[0].strip()
    raise SystemExit("Could not recover Prompt A v3 prefix from canonical_narrative_prompt_a_v3_vignettes.json")


def build_rows(source_rows: list[dict], prompt_a_prefix: str) -> list[dict]:
    built = []
    for row in source_rows:
        original = row["original_structured"].strip()
        stripped = strip_benchmark_artifacts(original)
        built.append(
            {
                **row,
                "source_stripped_original": stripped,
                "narrative_prompt_a_source_stripped": (
                    f"{prompt_a_prefix}\n\nPatient message:\n{stripped}"
                ),
            }
        )
    return built


def main() -> None:
    args = parse_args()
    source_rows = json.loads(args.input.read_text())
    v3_rows = json.loads(args.prompt_a_v3_input.read_text())
    prompt_a_prefix = extract_prompt_a_prefix(v3_rows)
    built = build_rows(source_rows, prompt_a_prefix)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(built, indent=2))
    print(f"Wrote {len(built)} rows to {args.output}")


if __name__ == "__main__":
    main()
