#!/bin/bash
set -euo pipefail

ROOT="/Users/david/debunking_nature/paper_faithful_triage_replication"
PROJECT="$ROOT"
WORKSPACE="$ROOT/paper_faithful_replication"
PYTHON_BIN="${PYTHON_BIN:-/Users/david/debunking_nature/triage_replication/.venv312/bin/python}"
ENV_FILE_PRIMARY="$PROJECT/.env"
ENV_FILE_FALLBACK="/Users/david/debunking_nature/triage_replication/.env"
DATASET="$WORKSPACE/data/canonical_source_stripped_vignettes.json"
RESULTS_DIR="$WORKSPACE/results"

RUNS="${RUNS:-1}"
CALL_WAIT="${CALL_WAIT:-1.0}"
OUTPUT_STEM="${OUTPUT_STEM:-source_stripped_original60_r${RUNS}}"

MODELS="${MODELS:-gpt-5.3-instant gpt-5.4-xhigh claude-sonnet-4.6 claude-opus-4.6 gemini-3-flash gemini-3.1-pro}"
FORMATS="${FORMATS:-source_stripped_original}"
ANTHROPIC_MAX_TOKENS="${ANTHROPIC_MAX_TOKENS:-4096}"

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

"$PYTHON_BIN" "$WORKSPACE/scripts/build_narrative_prompt_a_dataset.py" --variant v3
"$PYTHON_BIN" "$WORKSPACE/scripts/build_stripped_original_prompt_dataset.py"
mkdir -p "$RESULTS_DIR"

cd "$PROJECT"
"$PYTHON_BIN" run_natural_interaction.py \
  --models $MODELS \
  --formats $FORMATS \
  --runs "$RUNS" \
  --call-wait "$CALL_WAIT" \
  --anthropic-max-tokens "$ANTHROPIC_MAX_TOKENS" \
  --vignettes-path "$DATASET" \
  --output-dir "$RESULTS_DIR" \
  --output-stem "$OUTPUT_STEM"
