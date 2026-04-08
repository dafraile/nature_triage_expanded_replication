# Experiment Status Matrix

This matrix separates:

- what has already been run and can be interpreted now
- what was prepared but not yet run
- what does **not** need rerunning just because of the clinician rewrite review

## Short Answer

We do **not** need to rerun the canonical naturalistic `patient_realistic` bank simply because of the clinician review.

Reason:

- the clinician's final read was that Task 1 is generally good, with only a minor wording issue around `MH3`
- that issue does not materially affect the key DKA/asthma question
- therefore the previously completed canonical naturalistic runs remain valid for asking whether the original study pattern persists under our improved naturalistic rewrites

So the `DKA/asthma under-triage on canonical naturalistic vignettes` question is **already answered** by completed runs.

## Matrix

| ID | Condition | Input bank | Prompting style | Output style | Status | Main purpose | Main artifact(s) | Rerun needed? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S1` | Exact paper structured baseline | Canonical 60 | Original paper structured prompt | Forced paper `A/B/C/D` | Done | Faithful replication of original structured condition | [paper_faithful_singleturn_r2_20260314_013738_structured.csv](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/paper_faithful_singleturn_r2_20260314_013738_structured.csv) | No |
| `S2` | Canonical natural free-text baseline | Canonical 60 | `patient_realistic` natural rewrite | Free-text, then adjudicated | Done | Faithful naturalistic comparison against structured | [paper_faithful_singleturn_r2_20260314_013738_natural_adjudicated_paper.csv](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/paper_faithful_singleturn_r2_20260314_013738_natural_adjudicated_paper.csv) | No |
| `S3` | Structured vs natural canonical comparison | Canonical 60 | `S1` vs `S2` | Paired comparison | Done | Main faithful result | [paper_faithful_singleturn_r2_20260314_013738_comparison.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/paper_faithful_singleturn_r2_20260314_013738_comparison.json) | No |
| `S4` | Natural forced-letter follow-up | Canonical 60 | `patient_realistic` | Forced discrete triage letter | Done | Test whether natural free-text loss is partly output-mode related | [natural_forced_letter_r2_02_vs_pure_natural_comparison.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_forced_letter/results/natural_forced_letter_r2_02_vs_pure_natural_comparison.json) | No |
| `S5` | Natural forced-letter vs exact structured | Canonical 60 | Natural + forced-letter vs exact structured | Forced letter | Done | Compare classifier-style natural input against structured | [natural_forced_letter_r2_02_vs_exact_structured_comparison.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_forced_letter/results/natural_forced_letter_r2_02_vs_exact_structured_comparison.json) | No |
| `S6` | Prompt A v3 scaffold extension | Canonical 60 | `Prompt A v3` + current naturalistic bank | Explicit `Disposition:` + reasoning | Done | Test richer clinician-style scaffold on naturalistic inputs | Provider-specific result files in [results](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results) | No |
| `S7` | Prompt A v3, Claude thinking repaired | Canonical 60 | `Prompt A v3` + naturalistic bank | Explicit `Disposition:` + reasoning | Done | Clean Claude adaptive-thinking result after fixing token cap | [prompt_a_v3_claude60_thinking8192_r1.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/prompt_a_v3_claude60_thinking8192_r1.json) | No |
| `S8` | DKA bridge check | Legacy DKA + canonical E13/F13 | Legacy old scaffold | Internal letter scale | Done | Show old DKA result survives for legacy and canonical-with-labs; weakness is sparse symptoms-only F13 | [bridge_dka_r2_py312.csv](/Users/david/debunking_nature/triage_replication/results/bridge_dka/bridge_dka_r2_py312.csv) | No |
| `P1` | Canonical naturalistic `v2` rewrite bank | Canonical 60 | Revised naturalistic rewrites | Same as `S2` or `S6` | Prepared conceptually, not built | Would only be needed if clinician had required substantive rewrite changes | [NATURAL_REWRITE_V2_PATCHLIST.md](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/docs/NATURAL_REWRITE_V2_PATCHLIST.md) | **No, currently not needed** |
| `P2` | Source-stripped original wording | Canonical 60 | Paper wording with formatting artifacts removed | Free-text | Prepared, not run | Test whether benchmark artifacts, rather than case content, drive part of the effect | [canonical_source_stripped_vignettes.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/data/canonical_source_stripped_vignettes.json) | **Yes, if we want the next most important follow-up** |
| `P3` | Source-stripped original wording + Prompt A v3 | Canonical 60 | `Prompt A v3` layered onto stripped original wording | Explicit `Disposition:` + reasoning | Prepared, not run | Test scaffold on paper wording without benchmark-answer artifacts | [run_prompt_a_v3_source_stripped60.sh](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/run_prompt_a_v3_source_stripped60.sh) | **Yes, if we want the prompt-extension on original wording** |
| `P4` | Task 2 adjudicator clarification | Follow-up subset only | No model rerun | Human clarification | Pending | Separate literal output adjudication from clinician's own preferred triage | [task2_rows_for_followup_review.csv](/Users/david/debunking_nature/clinician_review_pack_20260320/task2_rows_for_followup_review.csv) | Not a model rerun |

## What Already Answers The DKA/Asthma Question

If the question is:

> Do the original study's difficult cases, especially DKA and asthma, still behave that way on our naturalistic, clinician-reviewed vignettes?

Then that is already answered by `S2`, because:

- `S2` used the same canonical naturalistic `patient_realistic` bank we just had reviewed
- the clinician did **not** request broad rewrite corrections
- therefore the `S2` results remain the operative answer for the current naturalistic bank

So:

- for the current naturalistic bank, **no rerun is required**
- for a new condition using different wording (`P2` or `P3`), a new run **would** be meaningful

## Recommended Next Steps

1. Treat the current naturalistic bank as frozen and acceptable.
2. Use the completed faithful canonical results as the main baseline.
3. Finish the human clarification follow-up for Task 2.
4. If we want one more high-value experiment, run `P2` first:
   - `source_stripped_original`
   - no benchmark answer-format artifacts
   - no Prompt A scaffold
5. After that, if useful, run `P3`:
   - `Prompt A v3` on the stripped-original wording

## Practical Interpretation

- `Current naturalistic bank`: good enough to keep
- `Need to rerun due to clinician rewrite concerns`: no
- `Most important unrun follow-up`: source-stripped original wording
- `Prompt-scaffolding extension`: already complete enough to analyze now
