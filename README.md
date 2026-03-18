# Paper-Faithful Triage Replication

This repository isolates the canonical replication pipeline built around the
paper's own `60` reference vignettes.

Scope:

- faithful single-turn replication on the paper-native `A/B/C/D` scale
- information-preserving natural single-turn rewrites
- forced-letter follow-up on the same canonical bank

This repo deliberately excludes the earlier mixed custom-bank experiments so the
dataset lineage and methods stay clean.

## Included Studies

### 1. Faithful single-turn study

Workspace:

- `paper_faithful_replication/`

Final analyzable run:

- exact structured paper prompts: `82.4%`
- natural free-text rewrites: `78.2%`
- matched-cell Wilcoxon: `p = 0.00354`

Interpretation:

- on this faithful `60`-case run, the exact structured prompt outperformed the
  free-text conversational rewrite
- the natural free-text condition increased under-triage, especially on the
  symptoms-only cases

Key files:

- `paper_faithful_replication/results/paper_faithful_singleturn_r2_20260314_013738_structured.csv`
- `paper_faithful_replication/results/paper_faithful_singleturn_r2_20260314_013738_natural_adjudicated_paper.csv`
- `paper_faithful_replication/results/paper_faithful_singleturn_r2_20260314_013738_comparison.json`

### 2. Natural forced-letter follow-up

Workspace:

- `paper_faithful_forced_letter/`

Final analyzable run:

- natural forced-letter: `84.2%`
- prior pure natural mean: `78.0%`
- Wilcoxon: `p = 6.61e-05`

Against the earlier exact structured run on the matched analyzable subset:

- natural forced-letter: `84.9%`
- exact structured: `82.2%`
- Wilcoxon: `p = 0.0269`

Interpretation:

- much of the free-text natural loss was tied to open-ended answer format, not
  just conversational input wording
- forcing a direct paper-scale letter helped substantially, especially on the
  symptoms-only cases

## Repository Layout

- `config.py`, `llm_utils.py`
  - shared model configuration and parsing helpers
- `run_natural_interaction.py`, `adjudicate_natural_interaction.py`
  - shared natural-response execution and adjudication utilities
- `paper_faithful_replication/`
  - canonical bank, rewrite workbook, faithful run scripts, final results
- `paper_faithful_forced_letter/`
  - forced-letter follow-up scripts and final results

## Setup

1. Create a Python environment.
2. Install dependencies from `requirements.txt`.
3. Copy `.env.example` to `.env` and fill in the API keys you need.

## Running

Faithful single-turn run:

```bash
./paper_faithful_replication/run_paper_faithful_overnight.sh
```

Natural forced-letter follow-up:

```bash
./paper_faithful_forced_letter/run_forced_letter_overnight.sh
```
