#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PFR_DIR="${PROJECT_ROOT}/paper_faithful_replication"
WORKSPACE_DIR="${SCRIPT_DIR}"
V2_SOURCE_JSON="${PFR_DIR}/data/canonical_singleturn_vignettes_clinician_v2.json"
DATASET_PATH="${WORKSPACE_DIR}/data/canonical_forced_letter_clinician_v2_vignettes.json"
RESULTS_DIR="${WORKSPACE_DIR}/results"
DEFAULT_PYTHON="/Users/david/debunking_nature/triage_replication/.venv312/bin/python"
ENV_FILE_PRIMARY="${PROJECT_ROOT}/.env"
ENV_FILE_FALLBACK="/Users/david/debunking_nature/triage_replication/.env"
PYTHON_BIN="${PYTHON_BIN:-}"
if [[ -z "${PYTHON_BIN}" ]]; then
  if [[ -x "${DEFAULT_PYTHON}" ]]; then
    PYTHON_BIN="${DEFAULT_PYTHON}"
  elif [[ -x "${PROJECT_ROOT}/.venv312/bin/python" ]]; then
    PYTHON_BIN="${PROJECT_ROOT}/.venv312/bin/python"
  else
    PYTHON_BIN="python3"
  fi
fi

RUNS="${RUNS:-2}"
CALL_WAIT="${CALL_WAIT:-1.0}"
OPENAI_MAX_COMPLETION_TOKENS="${OPENAI_MAX_COMPLETION_TOKENS:-4096}"
ANTHROPIC_MAX_TOKENS="${ANTHROPIC_MAX_TOKENS:-1024}"
RUN_LABEL="${RUN_LABEL:-paper_faithful_forced_letter_clinician_v2_r${RUNS}_$(date +%Y%m%d_%H%M%S)}"
MODELS_VALUE="${MODELS:-gpt-5.3-instant gpt-5.4-xhigh claude-sonnet-4.6 claude-opus-4.6 gemini-3-flash gemini-3.1-pro}"
FORMATS_VALUE="${FORMATS:-natural_forced_letter}"
CASES_VALUE="${CASES:-}"
GOOGLE_TRANSPORT="${GOOGLE_TRANSPORT:-vertex}"
DRY_RUN="${DRY_RUN:-0}"

declare -a MODEL_ARGS
declare -a FORMAT_ARGS
declare -a CASE_ARGS
declare -a CASE_OPTION
declare -a GOOGLE_FLAG
declare -a DRY_RUN_FLAG

read -r -a MODEL_ARGS <<< "${MODELS_VALUE}"
read -r -a FORMAT_ARGS <<< "${FORMATS_VALUE}"
if [[ -n "${CASES_VALUE}" ]]; then
  read -r -a CASE_ARGS <<< "${CASES_VALUE}"
fi
if [[ ${#CASE_ARGS[@]} -gt 0 ]]; then
  CASE_OPTION=(--cases "${CASE_ARGS[@]}")
fi

if [[ "${GOOGLE_TRANSPORT}" == "vertex" ]]; then
  GOOGLE_FLAG=(--google-vertex)
fi
if [[ "${DRY_RUN}" == "1" ]]; then
  DRY_RUN_FLAG=(--dry-run)
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

echo "======================================================================"
echo "  PAPER-FAITHFUL FORCED-LETTER EVAL (CLINICIAN V2)"
echo "======================================================================"
echo "  Models:  ${MODELS_VALUE}"
echo "  Formats: ${FORMATS_VALUE}"
echo "  Source:  ${V2_SOURCE_JSON}"
echo "  Dataset: ${DATASET_PATH}"
echo "  Runs:    ${RUNS}"
echo "  Cases:   ${CASES_VALUE:-all 60}"
echo "  Google:  ${GOOGLE_TRANSPORT}"
echo "  Dry run: ${DRY_RUN}"
echo "  Python:  ${PYTHON_BIN}"
echo "  Output:  ${RESULTS_DIR}"
echo "  Label:   ${RUN_LABEL}"
echo "======================================================================"

"${PYTHON_BIN}" "${PFR_DIR}/scripts/build_clinician_validated_naturalistic_v2.py" \
  --output "${V2_SOURCE_JSON}"

"${PYTHON_BIN}" "${WORKSPACE_DIR}/scripts/build_forced_letter_dataset.py" \
  --input-json "${V2_SOURCE_JSON}" \
  --output "${DATASET_PATH}"

run_cmd=(
  "${PYTHON_BIN}" "${WORKSPACE_DIR}/scripts/run_forced_letter_singleturn.py"
  --dataset "${DATASET_PATH}"
  --output-dir "${RESULTS_DIR}"
  --output-stem "${RUN_LABEL}_responses"
  --models "${MODEL_ARGS[@]}"
  --formats "${FORMAT_ARGS[@]}"
  --runs "${RUNS}"
  --call-wait "${CALL_WAIT}"
  --openai-max-completion-tokens "${OPENAI_MAX_COMPLETION_TOKENS}"
  --anthropic-max-tokens "${ANTHROPIC_MAX_TOKENS}"
)
if [[ ${#GOOGLE_FLAG[@]} -gt 0 ]]; then
  run_cmd+=("${GOOGLE_FLAG[@]}")
fi
if [[ ${#CASE_OPTION[@]} -gt 0 ]]; then
  run_cmd+=("${CASE_OPTION[@]}")
fi
if [[ ${#DRY_RUN_FLAG[@]} -gt 0 ]]; then
  run_cmd+=("${DRY_RUN_FLAG[@]}")
fi
"${run_cmd[@]}"

echo
if [[ "${DRY_RUN}" == "1" ]]; then
  echo "Dry run finished."
else
  echo "Finished. Key outputs:"
  echo "  ${RESULTS_DIR}/${RUN_LABEL}_responses.csv"
fi
