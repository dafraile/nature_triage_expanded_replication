**Working Summary**

This note consolidates the completed full-60 results as of 2026-04-08 after merging the clinician-v2 delta reruns for the 8 changed naturalistic cases:

- `E11`
- `E12`
- `E13`
- `MH3`
- `F6`
- `NH3`
- `E24`
- `F22`

The merged clinician-v2 full artifacts were built from:

- [paper_faithful_singleturn_clinician_v2_full_comparison.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/paper_faithful_singleturn_clinician_v2_full_comparison.json)
- [natural_forced_letter_clinician_v2_full_vs_exact_structured_comparison.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_forced_letter/results/natural_forced_letter_clinician_v2_full_vs_exact_structured_comparison.json)
- [natural_forced_letter_clinician_v2_full_vs_pure_natural_comparison.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_forced_letter/results/natural_forced_letter_clinician_v2_full_vs_pure_natural_comparison.json)
- [prompt_a_v3_clinician_v2_full_r1_20260408_summary.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/prompt_a_v3_clinician_v2_full_r1_20260408_summary.json)

**Replication Track**

Exact structured versus clinician-v2 natural free-text:

| Condition | Accuracy |
| --- | --- |
| Exact structured | `82.5%` |
| Natural free-text, GPT judge | `79.0%` |
| Natural free-text, Opus judge | `79.9%` |
| Natural free-text, two-judge mean | `79.4%` |

Main inference:

- The clinician-v2 naturalistic rerun remains below the exact structured condition.
- The gap is smaller than in the original v1 naturalistic run, but it does not reverse direction.
- Wilcoxon on cell-level mean accuracy remains significant in favor of structured:
  - `p = 0.0297`

By model:

| Model | Structured | Natural mean | Delta |
| --- | --- | --- | --- |
| `claude-opus-4.6` | `85.5%` | `76.5%` | `-9.0` pts |
| `claude-sonnet-4.6` | `81.1%` | `77.0%` | `-4.1` pts |
| `gemini-3-flash` | `81.2%` | `82.1%` | `+0.9` pts |
| `gemini-3.1-pro` | `84.0%` | `85.3%` | `+1.3` pts |
| `gpt-5.3-instant` | `81.4%` | `74.6%` | `-6.8` pts |
| `gpt-5.4-xhigh` | `82.2%` | `83.1%` | `+0.8` pts |

Files:

- [paper_faithful_singleturn_clinician_v2_full_rowwise.csv](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/paper_faithful_singleturn_clinician_v2_full_rowwise.csv)
- [paper_faithful_singleturn_clinician_v2_full_cell_summary.csv](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/paper_faithful_singleturn_clinician_v2_full_cell_summary.csv)

**Forced Letter**

Clinician-v2 natural forced-letter versus exact structured:

| Condition | Accuracy |
| --- | --- |
| Natural forced-letter | `85.2%` |
| Exact structured | `82.2%` |

Clinician-v2 natural forced-letter versus pure natural free-text:

| Condition | Accuracy |
| --- | --- |
| Natural forced-letter | `84.6%` |
| Pure natural free-text, GPT judge | `78.4%` |
| Pure natural free-text, Opus judge | `79.4%` |
| Pure natural free-text, two-judge mean | `78.9%` |

Main inference:

- Forced categorical output remains the strongest naturalistic replication condition.
- It outperforms both exact structured and pure natural free-text on matched rows.
- Against exact structured:
  - Wilcoxon `p = 0.0171`
  - McNemar exact `p = 0.00289`
- Against pure natural free-text:
  - Wilcoxon `p = 0.000170`

Files:

- [natural_forced_letter_clinician_v2_full_vs_exact_structured_comparison.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_forced_letter/results/natural_forced_letter_clinician_v2_full_vs_exact_structured_comparison.json)
- [natural_forced_letter_clinician_v2_full_vs_pure_natural_comparison.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_forced_letter/results/natural_forced_letter_clinician_v2_full_vs_pure_natural_comparison.json)

**Prompt A v3**

Clinician-v2 full-60 merged Prompt A v3 results:

| Model | Accuracy | With data | Symptoms only |
| --- | --- | --- | --- |
| `gpt-5.3-instant` | `90.0%` | `93.3%` | `86.7%` |
| `gpt-5.4-xhigh` | `88.3%` | `93.3%` | `83.3%` |
| `claude-opus-4.6-nothink` | `85.0%` | `90.0%` | `80.0%` |
| `claude-sonnet-4.6-nothink` | `85.0%` | `86.7%` | `83.3%` |
| `gpt-5.2-thinking-high` | `80.0%` | `83.3%` | `76.7%` |
| `claude-sonnet-4.6` | `76.7%` | `76.7%` | `76.7%` |
| `gemini-3-flash` | `73.3%` | `80.0%` | `66.7%` |
| `gemini-3.1-pro` | `60.0%` | `56.7%` | `63.3%` |
| `claude-opus-4.6` | `48.3%` | `50.0%` | `46.7%` |

Main inference:

- The Prompt A v3 pattern survives the clinician-v2 merge almost unchanged.
- OpenAI remains strongest.
- Claude non-thinking remains strong.
- Claude thinking remains worse than non-thinking.
- Opus thinking remains unusably over-triaging.

Files:

- [prompt_a_v3_clinician_v2_full_r1_20260408.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/prompt_a_v3_clinician_v2_full_r1_20260408.json)
- [prompt_a_v3_clinician_v2_full_r1_20260408_summary_by_model.csv](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/prompt_a_v3_clinician_v2_full_r1_20260408_summary_by_model.csv)

**Source-Stripped Originals**

Completed:

- raw baseline source-stripped run:
  - [source_stripped_original60_r1.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/source_stripped_original60_r1.json)
- adjudicated baseline:
  - [source_stripped_original60_r1_adjudicated_paper.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/source_stripped_original60_r1_adjudicated_paper.json)
- comparison against exact structured:
  - [source_stripped_original60_r1_vs_exact_structured_comparison.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/source_stripped_original60_r1_vs_exact_structured_comparison.json)
- Prompt A v3 on source-stripped originals:
  - [prompt_a_v3_source_stripped60_r1.json](/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/results/prompt_a_v3_source_stripped60_r1.json)

Source-stripped original wording versus exact structured:

| Condition | Accuracy |
| --- | --- |
| Exact structured | `81.8%` |
| Source-stripped, GPT judge | `79.2%` |
| Source-stripped, Opus judge | `82.4%` |
| Source-stripped, two-judge mean | `80.8%` |

Main inference:

- Removing the benchmark artifacts from the original paper wording closes most of the gap seen with the fully naturalistic rewrites.
- On the two-judge mean, source-stripped originals are only about `1` percentage point below exact structured.
- The Opus adjudicated view is actually slightly above the exact structured baseline, while the GPT adjudicated view is slightly below it.

Prompt A v3 on source-stripped originals, strict parsed:

| Model | Accuracy | With data | Symptoms only |
| --- | --- | --- | --- |
| `gpt-5.4-xhigh` | `86.7%` | `90.0%` | `83.3%` |
| `claude-opus-4.6-nothink` | `85.0%` | `90.0%` | `80.0%` |
| `claude-sonnet-4.6-nothink` | `85.0%` | `86.7%` | `83.3%` |
| `gpt-5.2-thinking-high` | `83.3%` | `86.7%` | `80.0%` |
| `gpt-5.3-instant` | `81.7%` | `83.3%` | `80.0%` |
| `gemini-3.1-pro` | `75.0%` | `73.3%` | `76.7%` |
| `gemini-3-flash` | `73.3%` | `80.0%` | `66.7%` |
