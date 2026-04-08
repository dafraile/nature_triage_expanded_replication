# Artifact-Stripped Original Prompt Condition

This condition is intended to test the paper's own case wording with benchmark-specific answer scaffolding removed, rather than using the later patient-style rewrites.

It is built from the canonical paper-faithful `source_prompt_text` / `original_structured` field and preserves:

- the original case facts
- the original ordering of information
- the original structured case wording

It removes only the benchmark artifacts that are not part of the clinical scenario itself:

- `Please base your answer only on the information in this message.`
- the entire `Please answer in exactly this format:` block
- the explicit `TRIAGE: <A/B/C/D ...>` response contract
- the confidence requirement
- the `If you would normally ask clarifying questions...` instruction

The resulting dataset exposes two new prompt fields:

- `source_stripped_original`
  - the paper's original case wording with the benchmark artifacts removed
- `narrative_prompt_a_source_stripped`
  - `Prompt A v3` prepended to `source_stripped_original`

This should be treated as a distinct experiment from both:

- exact structured paper replication (`original_structured`)
- naturalistic rewrite experiments (`patient_realistic`, `narrative_prompt_a`)

The goal is to isolate whether Prompt A v3 still helps when the model sees the paper's original wording and case structure, but without the forced output-format artifacts that may distort behavior.
