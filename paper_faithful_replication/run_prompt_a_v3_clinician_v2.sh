#!/bin/bash
set -euo pipefail

ROOT="/Users/david/debunking_nature/paper_faithful_triage_replication"
PROJECT="$ROOT"
WORKSPACE="$ROOT/paper_faithful_replication"
PYTHON_BIN="${PYTHON_BIN:-/Users/david/debunking_nature/triage_replication/.venv312/bin/python}"
ENV_FILE_PRIMARY="$PROJECT/.env"
ENV_FILE_FALLBACK="/Users/david/debunking_nature/triage_replication/.env"
SOURCE_DATASET="$WORKSPACE/data/canonical_singleturn_vignettes_clinician_v2.json"
DATASET="$WORKSPACE/data/canonical_narrative_prompt_a_v3_clinician_v2_vignettes.json"
RESULTS_DIR="$WORKSPACE/results"

RUNS="${RUNS:-1}"
CALL_WAIT="${CALL_WAIT:-1.0}"
ANTHROPIC_MAX_TOKENS="${ANTHROPIC_MAX_TOKENS:-8192}"
OUTPUT_STEM="${OUTPUT_STEM:-prompt_a_v3_clinician_v2_r${RUNS}}"
CASES_VALUE="${CASES:-}"
DRY_RUN="${DRY_RUN:-0}"

MODELS="${MODELS:-claude-sonnet-4.6-nothink claude-sonnet-4.6 claude-opus-4.6-nothink claude-opus-4.6 gpt-5.2-thinking-high gpt-5.3-instant gpt-5.4-xhigh gemini-3-flash gemini-3.1-pro}"
FORMATS="${FORMATS:-narrative_prompt_a}"

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Python interpreter not found: $PYTHON_BIN" >&2
  exit 1
fi

if [ -f "$ENV_FILE_PRIMARY" ]; then
  set -a
  . "$ENV_FILE_PRIMARY"
  set +a
elif [ -f "$ENV_FILE_FALLBACK" ]; then
  set -a
  . "$ENV_FILE_FALLBACK"
  set +a
fi

CASE_FLAGS=()
DRY_RUN_FLAG=()
if [ -n "$CASES_VALUE" ]; then
  read -r -a CASE_ARGS <<< "$CASES_VALUE"
  CASE_FLAGS+=(--cases "${CASE_ARGS[@]}")
fi
if [ "$DRY_RUN" = "1" ]; then
  DRY_RUN_FLAG+=(--dry-run)
fi

"$PYTHON_BIN" "$WORKSPACE/scripts/build_clinician_validated_naturalistic_v2.py" \
  --output "$SOURCE_DATASET"
"$PYTHON_BIN" "$WORKSPACE/scripts/build_narrative_prompt_a_dataset.py" \
  --variant v3 \
  --input "$SOURCE_DATASET" \
  --output "$DATASET"
mkdir -p "$RESULTS_DIR"

cd "$PROJECT"
run_cmd=(
  "$PYTHON_BIN" run_natural_interaction.py
  --models $MODELS
  --formats $FORMATS
  --runs "$RUNS"
  --call-wait "$CALL_WAIT"
  --anthropic-max-tokens "$ANTHROPIC_MAX_TOKENS"
  --vignettes-path "$DATASET"
  --output-dir "$RESULTS_DIR"
  --output-stem "$OUTPUT_STEM"
)
if [ ${#CASE_FLAGS[@]} -gt 0 ]; then
  run_cmd+=("${CASE_FLAGS[@]}")
fi
if [ ${#DRY_RUN_FLAG[@]} -gt 0 ]; then
  run_cmd+=("${DRY_RUN_FLAG[@]}")
fi
"${run_cmd[@]}"
