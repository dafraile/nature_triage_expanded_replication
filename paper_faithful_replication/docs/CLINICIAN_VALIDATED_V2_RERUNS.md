# Clinician-Validated V2 Reruns

This document defines the reruns required if the approved target dataset is the
patched clinician-validated naturalistic bank rather than the original
`patient_realistic` bank.

## Frozen v2 dataset

Builder:

- `/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/scripts/build_clinician_validated_naturalistic_v2.py`

Output:

- `/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/data/canonical_singleturn_vignettes_clinician_v2.json`

Patched cases:

- `E11`
- `E12`
- `E13`
- `MH3`
- `F6`
- `NH3`
- `E24`
- `F22`

## Conditions that must be rerun

These conditions depend on `patient_realistic` or prompt scaffolds built from it.

1. Canonical natural free-text baseline
2. Natural forced-letter follow-up
3. `Prompt A v3` on the naturalistic bank

## Conditions that do not need rerunning

These do not depend on the naturalistic rewrite text.

1. Exact structured paper baseline
2. `source_stripped_original` baseline
3. `Prompt A v3 + source_stripped_original`

## Launchers

Natural free-text baseline:

- `/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/run_clinician_validated_natural_v2.sh`

Prompt A v3 on clinician-v2 naturalistic bank:

- `/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/run_prompt_a_v3_clinician_v2.sh`

Natural forced-letter on clinician-v2 naturalistic bank:

- `/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_forced_letter/run_forced_letter_clinician_v2.sh`

## Ready-to-run commands

Natural free-text baseline:

```bash
cd /Users/david/debunking_nature/paper_faithful_triage_replication
/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/run_clinician_validated_natural_v2.sh
```

Prompt A v3:

```bash
cd /Users/david/debunking_nature/paper_faithful_triage_replication
/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/run_prompt_a_v3_clinician_v2.sh
```

Forced-letter:

```bash
cd /Users/david/debunking_nature/paper_faithful_triage_replication
/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_forced_letter/run_forced_letter_clinician_v2.sh
```

## Optional smoke tests

Natural free-text:

```bash
cd /Users/david/debunking_nature/paper_faithful_triage_replication
CASES='E1' DRY_RUN=1 MODELS='gpt-5.3-instant' RUN_LABEL='clinician_v2_smoke' \
/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/run_clinician_validated_natural_v2.sh
```

Prompt A v3:

```bash
cd /Users/david/debunking_nature/paper_faithful_triage_replication
CASES='E1' DRY_RUN=1 MODELS='gpt-5.3-instant' OUTPUT_STEM='prompt_a_v3_clinician_v2_smoke' \
/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_replication/run_prompt_a_v3_clinician_v2.sh
```

Forced-letter:

```bash
cd /Users/david/debunking_nature/paper_faithful_triage_replication
CASES='E1' DRY_RUN=1 MODELS='gpt-5.3-instant' RUN_LABEL='forced_letter_clinician_v2_smoke' \
/Users/david/debunking_nature/paper_faithful_triage_replication/paper_faithful_forced_letter/run_forced_letter_clinician_v2.sh
```
