#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
WORKSPACE_DIR="${PROJECT_ROOT}/paper_faithful_replication"
RESULTS_DIR="${WORKSPACE_DIR}/results"
DATASET_JSON="${WORKSPACE_DIR}/data/canonical_singleturn_vignettes_clinician_v2.json"
STRUCTURED_REFERENCE="${STRUCTURED_REFERENCE:-${RESULTS_DIR}/paper_faithful_singleturn_r2_20260314_013738_structured.csv}"
ENV_FILE_PRIMARY="${PROJECT_ROOT}/.env"
ENV_FILE_FALLBACK="/Users/david/debunking_nature/triage_replication/.env"

if [[ -x "/Users/david/debunking_nature/triage_replication/.venv312/bin/python" ]]; then
  PYTHON_BIN="/Users/david/debunking_nature/triage_replication/.venv312/bin/python"
elif [[ -x "${PROJECT_ROOT}/.venv312/bin/python" ]]; then
  PYTHON_BIN="${PROJECT_ROOT}/.venv312/bin/python"
else
  PYTHON_BIN="${PYTHON_BIN:-python3}"
fi

RUNS="${RUNS:-2}"
CALL_WAIT="${CALL_WAIT:-1.5}"
OPENAI_SOURCE_MAX_COMPLETION_TOKENS="${OPENAI_SOURCE_MAX_COMPLETION_TOKENS:-8192}"
OPENAI_JUDGE_MAX_COMPLETION_TOKENS="${OPENAI_JUDGE_MAX_COMPLETION_TOKENS:-4096}"
ANTHROPIC_SOURCE_MAX_TOKENS="${ANTHROPIC_SOURCE_MAX_TOKENS:-4096}"
ANTHROPIC_JUDGE_MAX_TOKENS="${ANTHROPIC_JUDGE_MAX_TOKENS:-2048}"
GOOGLE_TRANSPORT="${GOOGLE_TRANSPORT:-vertex}"
RUN_LABEL="${RUN_LABEL:-paper_faithful_clinician_v2_natural_r${RUNS}_$(date +%Y%m%d_%H%M%S)}"
CASES_VALUE="${CASES:-}"
DRY_RUN="${DRY_RUN:-0}"

MODELS=(
  "gpt-5.3-instant"
  "gpt-5.4-xhigh"
  "claude-sonnet-4.6"
  "claude-opus-4.6"
  "gemini-3-flash"
  "gemini-3.1-pro"
)

NATURAL_STEM="${RUN_LABEL}_natural"
NATURAL_ADJUDICATED_CSV="${RESULTS_DIR}/${NATURAL_STEM}_adjudicated_paper.csv"

GOOGLE_FLAGS=()
CASE_FLAGS=()
DRY_RUN_FLAG=()
if [[ "${GOOGLE_TRANSPORT}" == "vertex" ]]; then
  GOOGLE_FLAGS+=(--google-vertex)
fi
if [[ -n "${CASES_VALUE}" ]]; then
  read -r -a CASE_ARGS <<< "${CASES_VALUE}"
  CASE_FLAGS+=(--cases "${CASE_ARGS[@]}")
fi
if [[ "${DRY_RUN}" == "1" ]]; then
  DRY_RUN_FLAG+=(--dry-run)
fi

if [[ -f "${ENV_FILE_PRIMARY}" ]]; then
  set -a
  . "${ENV_FILE_PRIMARY}"
  set +a
elif [[ -f "${ENV_FILE_FALLBACK}" ]]; then
  set -a
  . "${ENV_FILE_FALLBACK}"
  set +a
fi

mkdir -p "${RESULTS_DIR}"

echo "Clinician-validated v2 natural rerun"
echo "  Python: ${PYTHON_BIN}"
echo "  Runs per cell: ${RUNS}"
echo "  Models: ${MODELS[*]}"
echo "  Google transport: ${GOOGLE_TRANSPORT}"
echo "  Run label: ${RUN_LABEL}"
echo "  Dataset: ${DATASET_JSON}"
echo "  Cases: ${CASES_VALUE:-all 60}"
echo "  Dry run: ${DRY_RUN}"
echo "  Structured reference: ${STRUCTURED_REFERENCE}"
echo

echo "[1/4] Building clinician-validated v2 dataset"
"${PYTHON_BIN}" "${WORKSPACE_DIR}/scripts/build_clinician_validated_naturalistic_v2.py"

echo
echo "[2/4] Running natural single-turn rewrites on clinician-validated v2"
run_cmd=(
  "${PYTHON_BIN}" "${PROJECT_ROOT}/run_natural_interaction.py"
  --models "${MODELS[@]}"
  --formats patient_realistic
  --runs "${RUNS}"
  --vignettes-path "${DATASET_JSON}"
  --output-dir "${RESULTS_DIR}"
  --output-stem "${NATURAL_STEM}"
  --openai-max-completion-tokens "${OPENAI_SOURCE_MAX_COMPLETION_TOKENS}"
  --anthropic-max-tokens "${ANTHROPIC_SOURCE_MAX_TOKENS}"
  --call-wait "${CALL_WAIT}"
)
if [[ ${#CASE_FLAGS[@]} -gt 0 ]]; then
  run_cmd+=("${CASE_FLAGS[@]}")
fi
if [[ ${#DRY_RUN_FLAG[@]} -gt 0 ]]; then
  run_cmd+=("${DRY_RUN_FLAG[@]}")
fi
if [[ ${#GOOGLE_FLAGS[@]} -gt 0 ]]; then
  run_cmd+=("${GOOGLE_FLAGS[@]}")
fi
"${run_cmd[@]}"

if [[ "${DRY_RUN}" == "1" ]]; then
  echo
  echo "Dry run finished."
  exit 0
fi

echo
echo "[3/4] Adjudicating natural replies"
"${PYTHON_BIN}" "${WORKSPACE_DIR}/scripts/adjudicate_natural_paper_scale.py" \
  --input "${RESULTS_DIR}/${NATURAL_STEM}.csv" \
  --vignettes-path "${DATASET_JSON}" \
  --output-dir "${RESULTS_DIR}" \
  --adjudicators gpt-5.4-xhigh claude-opus-4.6 \
  --openai-max-completion-tokens "${OPENAI_JUDGE_MAX_COMPLETION_TOKENS}" \
  --anthropic-max-tokens "${ANTHROPIC_JUDGE_MAX_TOKENS}" \
  --call-wait "${CALL_WAIT}"

echo
echo "[4/4] Comparing structured vs clinician-validated v2 natural"
"${PYTHON_BIN}" "${WORKSPACE_DIR}/scripts/compare_structured_vs_natural_singleturn.py" \
  --structured "${STRUCTURED_REFERENCE}" \
  --natural "${NATURAL_ADJUDICATED_CSV}" \
  --output-dir "${RESULTS_DIR}" \
  --run-label "${RUN_LABEL}" \
  --judge-models gpt-5.4-xhigh claude-opus-4.6

echo
echo "Done."
echo "Natural CSV: ${RESULTS_DIR}/${NATURAL_STEM}.csv"
echo "Adjudicated natural CSV: ${NATURAL_ADJUDICATED_CSV}"
echo "Comparison JSON: ${RESULTS_DIR}/${RUN_LABEL}_comparison.json"
