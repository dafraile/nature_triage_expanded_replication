#!/usr/bin/env python3
"""Merge clinician-v2 delta reruns into the full naturalistic result artifacts."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
PROJECT = WORKSPACE.parent
FORCED_DIR = PROJECT / "paper_faithful_forced_letter"
RESULTS = WORKSPACE / "results"
FORCED_RESULTS = FORCED_DIR / "results"

ORIGINAL_STRUCTURED_CSV = RESULTS / "paper_faithful_singleturn_r2_20260314_013738_structured.csv"
ORIGINAL_NATURAL_JSON = RESULTS / "paper_faithful_singleturn_r2_20260314_013738_natural.json"
ORIGINAL_NATURAL_CSV = RESULTS / "paper_faithful_singleturn_r2_20260314_013738_natural.csv"
ORIGINAL_NATURAL_ADJ_JSON = RESULTS / "paper_faithful_singleturn_r2_20260314_013738_natural_adjudicated_paper.json"
ORIGINAL_NATURAL_ADJ_CSV = RESULTS / "paper_faithful_singleturn_r2_20260314_013738_natural_adjudicated_paper.csv"
DELTA_NATURAL_JSON = RESULTS / "paper_faithful_clinician_v2_delta8_r2_20260408_natural.json"
DELTA_NATURAL_ADJ_JSON = RESULTS / "paper_faithful_clinician_v2_delta8_r2_20260408_natural_adjudicated_paper.json"

ORIGINAL_FORCED_JSON = FORCED_RESULTS / "natural_forced_letter_r2_02_responses.json"
ORIGINAL_FORCED_CSV = FORCED_RESULTS / "natural_forced_letter_r2_02_responses.csv"
DELTA_FORCED_JSON = FORCED_RESULTS / "paper_faithful_forced_letter_clinician_v2_delta8_r2_20260408_responses.json"

PROMPT_A_SOURCE_FILES = [
    RESULTS / "prompt_a_v3_openai60_r1.json",
    RESULTS / "prompt_a_v3_google60_r1.json",
]
PROMPT_A_CLAUDE_NOTHINK = RESULTS / "prompt_a_v3_claude60_r1.json"
PROMPT_A_CLAUDE_THINK = RESULTS / "prompt_a_v3_claude60_thinking8192_r1.json"
PROMPT_A_DELTA_JSON = RESULTS / "prompt_a_v3_clinician_v2_delta8_r1_20260408.json"

NATURAL_FULL_STEM = "paper_faithful_singleturn_clinician_v2_full"
FORCED_FULL_STEM = "natural_forced_letter_clinician_v2_full"
PROMPT_A_FULL_STEM = "prompt_a_v3_clinician_v2_full_r1_20260408"


def load_rows(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text())
    if path.suffix.lower() == ".csv":
        with path.open(newline="") as f:
            return list(csv.DictReader(f))
    raise ValueError(f"Unsupported file type: {path}")


def write_rows(rows: list[dict], json_path: Path, csv_path: Path) -> None:
    json_path.write_text(json.dumps(rows, indent=2, default=str))
    if rows:
        with csv_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def key_for_row(row: dict) -> tuple[str, str, str, str]:
    model = row.get("source_model") or row.get("model")
    return (
        str(model),
        str(row["case_id"]),
        str(row["prompt_format"]),
        str(row["run_number"]),
    )


def merge_rows(base_rows: list[dict], delta_rows: list[dict]) -> list[dict]:
    delta_by_key = {key_for_row(row): row for row in delta_rows}
    merged: list[dict] = []
    seen: set[tuple[str, str, str, str]] = set()

    for row in base_rows:
        key = key_for_row(row)
        if key in delta_by_key:
            merged.append(delta_by_key[key])
        else:
            merged.append(row)
        seen.add(key)

    for key, row in delta_by_key.items():
        if key not in seen:
            merged.append(row)

    merged.sort(key=lambda row: key_for_row(row))
    return merged


def run_python(script: Path, *args: str) -> None:
    cmd = [sys.executable, str(script), *args]
    subprocess.run(cmd, check=True, cwd=PROJECT)


def merge_natural() -> tuple[Path, Path]:
    natural_rows = merge_rows(load_rows(ORIGINAL_NATURAL_JSON), load_rows(DELTA_NATURAL_JSON))
    natural_json = RESULTS / f"{NATURAL_FULL_STEM}_natural.json"
    natural_csv = RESULTS / f"{NATURAL_FULL_STEM}_natural.csv"
    write_rows(natural_rows, natural_json, natural_csv)

    adjudicated_rows = merge_rows(load_rows(ORIGINAL_NATURAL_ADJ_JSON), load_rows(DELTA_NATURAL_ADJ_JSON))
    natural_adj_json = RESULTS / f"{NATURAL_FULL_STEM}_natural_adjudicated_paper.json"
    natural_adj_csv = RESULTS / f"{NATURAL_FULL_STEM}_natural_adjudicated_paper.csv"
    write_rows(adjudicated_rows, natural_adj_json, natural_adj_csv)

    run_python(
        WORKSPACE / "scripts" / "compare_structured_vs_natural_singleturn.py",
        "--structured", str(ORIGINAL_STRUCTURED_CSV),
        "--natural", str(natural_adj_csv),
        "--output-dir", str(RESULTS),
        "--run-label", NATURAL_FULL_STEM,
        "--structured-format", "original_structured",
        "--natural-format", "patient_realistic",
        "--judge-models", "gpt-5.4-xhigh", "claude-opus-4.6",
    )
    return natural_csv, natural_adj_csv


def merge_forced(pure_natural_adjudicated_csv: Path) -> Path:
    forced_rows = merge_rows(load_rows(ORIGINAL_FORCED_JSON), load_rows(DELTA_FORCED_JSON))
    forced_json = FORCED_RESULTS / f"{FORCED_FULL_STEM}_responses.json"
    forced_csv = FORCED_RESULTS / f"{FORCED_FULL_STEM}_responses.csv"
    write_rows(forced_rows, forced_json, forced_csv)

    run_python(
        FORCED_DIR / "scripts" / "compare_forced_letter_vs_exact_structured.py",
        "--forced", str(forced_csv),
        "--structured", str(ORIGINAL_STRUCTURED_CSV),
        "--output-dir", str(FORCED_RESULTS),
        "--run-label", f"{FORCED_FULL_STEM}_vs_exact_structured",
        "--forced-format", "natural_forced_letter",
        "--structured-format", "original_structured",
    )
    run_python(
        FORCED_DIR / "scripts" / "compare_forced_letter_vs_pure_natural.py",
        "--forced", str(forced_csv),
        "--pure-natural", str(pure_natural_adjudicated_csv),
        "--output-dir", str(FORCED_RESULTS),
        "--run-label", f"{FORCED_FULL_STEM}_vs_pure_natural",
        "--forced-format", "natural_forced_letter",
        "--pure-format", "patient_realistic",
        "--judge-models", "gpt-5.4-xhigh", "claude-opus-4.6",
    )
    return forced_csv


def load_prompt_a_base_rows() -> list[dict]:
    rows: list[dict] = []
    for path in PROMPT_A_SOURCE_FILES:
        rows.extend(load_rows(path))

    rows.extend(
        row for row in load_rows(PROMPT_A_CLAUDE_NOTHINK)
        if str(row["model"]).endswith("-nothink")
    )
    rows.extend(
        row for row in load_rows(PROMPT_A_CLAUDE_THINK)
        if str(row["model"]) in {"claude-sonnet-4.6", "claude-opus-4.6"}
    )
    return rows


def to_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def classify_case_bucket(case_id: str) -> str:
    if case_id.startswith("E") or case_id.startswith("MH"):
        return "with_data"
    if case_id.startswith("F") or case_id.startswith("NH"):
        return "symptoms_only"
    return "other"


def summarize_prompt_a(rows: Iterable[dict]) -> tuple[list[dict], dict]:
    rows = list(rows)
    by_model: dict[str, list[dict]] = {}
    for row in rows:
        by_model.setdefault(str(row["model"]), []).append(row)

    summary_rows: list[dict] = []
    for model in sorted(by_model):
        items = by_model[model]
        total = len(items)
        correct = sum(1 for row in items if to_bool(row.get("best_effort_is_correct")))
        with_data = [row for row in items if classify_case_bucket(str(row["case_id"])) == "with_data"]
        symptoms_only = [row for row in items if classify_case_bucket(str(row["case_id"])) == "symptoms_only"]
        summary_rows.append(
            {
                "model": model,
                "n": total,
                "correct": correct,
                "accuracy": correct / total if total else None,
                "with_data_n": len(with_data),
                "with_data_correct": sum(1 for row in with_data if to_bool(row.get("best_effort_is_correct"))),
                "with_data_accuracy": (
                    sum(1 for row in with_data if to_bool(row.get("best_effort_is_correct"))) / len(with_data)
                    if with_data else None
                ),
                "symptoms_only_n": len(symptoms_only),
                "symptoms_only_correct": sum(1 for row in symptoms_only if to_bool(row.get("best_effort_is_correct"))),
                "symptoms_only_accuracy": (
                    sum(1 for row in symptoms_only if to_bool(row.get("best_effort_is_correct"))) / len(symptoms_only)
                    if symptoms_only else None
                ),
            }
        )

    overall = {
        "n_rows": len(rows),
        "n_models": len(by_model),
    }
    return summary_rows, overall


def merge_prompt_a() -> Path:
    prompt_a_rows = merge_rows(load_prompt_a_base_rows(), load_rows(PROMPT_A_DELTA_JSON))
    prompt_a_json = RESULTS / f"{PROMPT_A_FULL_STEM}.json"
    prompt_a_csv = RESULTS / f"{PROMPT_A_FULL_STEM}.csv"
    write_rows(prompt_a_rows, prompt_a_json, prompt_a_csv)

    summary_rows, overall = summarize_prompt_a(prompt_a_rows)
    summary_csv = RESULTS / f"{PROMPT_A_FULL_STEM}_summary_by_model.csv"
    with summary_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)
    summary_json = RESULTS / f"{PROMPT_A_FULL_STEM}_summary.json"
    summary_json.write_text(json.dumps({"overall": overall, "by_model": summary_rows}, indent=2))
    return prompt_a_csv


def main() -> None:
    _, natural_adj_csv = merge_natural()
    merge_forced(natural_adj_csv)
    merge_prompt_a()
    print("Built clinician-v2 full natural, forced-letter, and Prompt A artifacts.")


if __name__ == "__main__":
    main()
