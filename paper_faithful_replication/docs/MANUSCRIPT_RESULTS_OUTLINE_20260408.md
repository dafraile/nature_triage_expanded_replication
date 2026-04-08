**Results Outline**

**1. Exact Structured Replication**

We first reproduced the paper-faithful exact structured condition on the full canonical bank. This provides the anchor condition for all downstream comparisons. In the merged clinician-v2 full comparison, the exact structured condition achieved `82.5%` matched-row accuracy, establishing that the benchmark is not trivially easy but also not catastrophically poor under direct replication.

Suggested framing:

- “On the full canonical single-turn benchmark, the exact structured condition achieved `82.5%` matched-row accuracy.”
- “This exact structured condition served as the reference for all naturalized and scaffolded comparisons.”

**2. Clinician-Validated Naturalistic Rewrites**

We then evaluated clinician-reviewed naturalistic rewrites of the same canonical cases. Performance remained below the exact structured benchmark, but the gap narrowed relative to the earlier v1 naturalistic run. In the clinician-v2 merged full comparison, natural free-text reached `79.0%` under GPT adjudication, `79.9%` under Claude adjudication, and `79.4%` on the two-judge mean, versus `82.5%` for exact structured.

The naturalistic free-text condition separated sharply by information type. On the pooled two-judge mean, cases with objective data (`E` + `MH`) reached `83.7%`, whereas symptoms-only cases (`F` + `NH`) reached `71.9%`. This pattern was visible in every model family, with the largest drop on symptoms-only rows in `gpt-5.3-instant` (`82.5%` with data vs `65.0%` symptoms-only) and the smallest in `gpt-5.4-xhigh` (`84.2%` vs `79.2%`).

Suggested framing:

- “Clinician-validated naturalistic rewrites did not surpass the exact structured benchmark.”
- “The two-judge mean naturalistic accuracy was `79.4%`, compared with `82.5%` for the exact structured condition.”
- “The direction of effect therefore remained unfavorable to fully naturalized free-text input, although the gap was smaller than in the original v1 rewrite set.”

Statistical language:

- “Cell-level Wilcoxon comparison remained significant in favor of exact structured (`p = 0.0297`).”

Error direction was mixed rather than purely under-triage. Across both judges combined:

- with-data judgments: `35` under-triages and `71` over-triages
- symptoms-only judgments: `101` under-triages and `94` over-triages
- overall: `136` under-triages and `165` over-triages

Suggested interpretation:

- “Naturalistic free-text errors were slightly over-triage-dominant overall, but this aggregate concealed an important split: with-data cases skewed toward over-triage, whereas under-triage concentrated disproportionately in symptoms-only presentations.”

**3. Source-Stripped Original Wording**

To isolate the role of benchmark artifacts, we removed the original paper’s answer-formatting constraints while preserving the original case wording and information order. This source-stripped condition nearly matched the exact structured benchmark: `79.2%` under GPT adjudication, `82.4%` under Claude adjudication, and `80.8%` on the two-judge mean, versus `81.8%` exact structured on matched rows.

Suggested framing:

- “Removing the benchmark artifacts from the original wording closed most of the gap between exact structured and naturalized input.”
- “The two-judge mean for source-stripped originals (`80.8%`) was within about 1 percentage point of the exact structured benchmark (`81.8%`).”
- “This suggests that much of the degradation observed under full naturalization is attributable to the rewrite into realistic patient language rather than merely to removal of the benchmark’s explicit answer scaffolding.”

**4. Forced-Letter Naturalistic Condition**

We next tested a naturalistic condition that preserved patient-language input while constraining output to the paper’s categorical triage scale. This was the strongest condition in the replication track. On matched rows, clinician-v2 natural forced-letter achieved `85.2%` versus `82.2%` for exact structured, and `84.6%` versus `78.9%` for pure natural free-text.

Suggested framing:

- “Naturalistic input paired with explicit categorical output outperformed both the exact structured benchmark and the unconstrained natural free-text condition.”
- “Against exact structured, forced-letter achieved `85.2%` versus `82.2%` (`p = 0.0171`, Wilcoxon; McNemar exact `p = 0.00289`).”
- “Against pure natural free-text, forced-letter achieved `84.6%` versus `78.9%` on the two-judge mean (`p = 0.000170`, Wilcoxon).”

Interpretation sentence:

- “This pattern indicates that the most damaging component is not patient-language input per se, but the combination of unconstrained free-text output with harder-to-parse recommendation structure.”

**5. Prompt-Scaffold Extension (Prompt A v3)**

As a separate extension, we tested a richer clinician-style scaffold on the canonical bank. This is not part of the core replication, but an intervention study asking whether prompt design can improve triage calibration. Performance was highly model-dependent. The strongest models were OpenAI (`gpt-5.3-instant` `90.0%`, `gpt-5.4-xhigh` `88.3%`), followed by Claude non-thinking variants (`85.0%` each for Sonnet and Opus). Claude thinking variants underperformed their non-thinking counterparts, and Opus thinking collapsed into marked over-triage (`48.3%` overall).

Suggested framing:

- “Prompt scaffolding can improve performance substantially for some models, but its effect is model-family- and reasoning-mode-dependent.”
- “OpenAI models benefited most from the scaffold, whereas Claude thinking variants deteriorated, with Opus thinking showing pervasive over-triage.”

**6. Failure Structure**

The main replication-track residual failures were not dominated by a single emergency pattern. Instead:

- fully naturalized free-text retained a modest deficit relative to exact structured
- source-stripped originals were close to exact structured
- forced-letter naturalistic was strongest

In the scaffold extension, failure patterns were concentrated in:

- benign cases upgraded from self-care to routine review
- symptoms-only asthma and early compensated acute presentations
- over-triage under some thinking-enabled Claude conditions

Suggested framing:

- “Residual disagreement was concentrated in boundary cases, especially self-care versus routine review, and in sparse symptoms-only acute presentations.”
- “The most severe scaffold-specific failure mode was not under-triage but over-triage under Claude thinking configurations.”

**7. Comparison to the Original Preprint**

The new full canonical results support the core mechanistic intuition of the original preprint, but they materially refine its strength and scope.

Supported:

- DKA under-triage is not a stable general LLM failure.
- Output format matters.
- Forced categorical output can improve measurable triage performance relative to free-form free-text.
- Symptoms-only asthma remains one of the most fragile benchmark cases.

Refined or weakened:

- The original preprint argued more strongly that natural free-text interaction rescues emergency triage failure. On the full canonical bank, that does not hold as a general statement.
- Fully naturalized free-text remains slightly worse than exact structured on the full benchmark.
- The stronger and more defensible statement is now that benchmark behavior is highly sensitive to prompt/input/output formatting, and that the source-stripped and forced-letter conditions perform much closer to or better than the exact structured benchmark than the fully naturalized free-text condition does.

Concrete contrast with the original preprint:

- Original 17-case/custom-bank preprint:
  - matched natural interaction outperformed constrained evaluation (`70.1%` vs `63.6%`)
  - DKA remained `100%` in both
  - asthma improved materially (`37/50` to `45/50`; realistic asthma `12/25` to `20/25`)
- Full canonical clinician-v2 replication:
  - exact structured outperformed fully naturalized free-text (`82.5%` vs `79.4%`)
  - source-stripped originals nearly matched exact structured (`80.8%`)
  - naturalistic forced-letter outperformed both (`85.2%` vs `82.2%` exact structured; `84.6%` vs `78.9%` pure natural)

Suggested wording:

- “The full canonical replication narrows but does not eliminate the original preprint’s core claim. We continue to find that evaluation behavior is highly format-sensitive, but the strongest broad statement is no longer that free-text natural interaction uniformly rescues performance. Rather, the data now support a more specific conclusion: performance depends strongly on the interaction between input naturalization, output discretization, and benchmark scaffolding.”

**8. One-Paragraph Results Summary**

Suggested compact paragraph:

“On the full canonical benchmark, the exact structured condition achieved `82.5%` matched-row accuracy. Clinician-validated naturalistic free-text rewrites remained modestly lower (`79.4%` two-judge mean), whereas source-stripped originals nearly matched the exact structured benchmark (`80.8%` two-judge mean). A naturalistic forced-letter condition outperformed both exact structured (`85.2%` vs `82.2%`) and pure natural free-text (`84.6%` vs `78.9%`). In a separate prompt-scaffold extension, performance was highly model-dependent: OpenAI models improved substantially under the scaffold, Claude non-thinking variants remained strong, and Claude thinking variants worsened through over-triage. Taken together, these results indicate that reported triage performance is highly sensitive to prompt/input/output format, and that the benchmark’s original structured scaffold should not be treated as a neutral readout of underlying triage capability.” 
