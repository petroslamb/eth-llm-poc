# III. What the Runs Actually Show

With evidence rules in place, we can now separate three things that are often conflated:

1. output fluency,
2. output completeness,
3. output trustworthiness.

This section focuses on observed patterns in current artifacts and scored samples, not broad architecture forecasts.

---

## 1) Finding: Model Differences Are Primarily Error-Profile Differences

The strongest supported claim is not "model X is globally best."

The strongest claim is:

> Different models fail in different ways, and those ways matter more than superficial output polish.

### Sample-backed signal
From `docs/evaluations/sample_scored_run.csv` / `docs/evaluations/metrics_summary.md`:
- Haiku sample (49 rows in expanded view): average score 3.5/10, with 39 `invalid`, 1 `disputed`.
- Opus sample (20 rows: EIP-1559 + EIP-2930): average score 9.4/10, with 0 `invalid`, 1 `disputed`.
- Sonnet sample (12 rows, EIP-1559): average score 9.0/10, with 0 `invalid`, 1 `disputed`.
- Direct-adjudication subset (excluding compare-derived rows): Haiku remains 5.0/10 across 15 rows.

This is a strong directional signal in sample evidence, not a full benchmark; compare-derived rows are intentionally conservative proxy scoring.

### Qualitative-evaluation alignment
The sample pattern aligns with qualitative findings:
- Haiku: high mapping noise and many unrelated client paths (`poc5/docs/QUALITATIVE_EVALUATION.md:35-36`).
- Opus: strongest practical quality but with incompleteness and at least one contested obligation (`poc5/docs/QUALITATIVE_EVALUATION.md:39-43`).

### Concrete Haiku failure mode
In spot-check evidence, Haiku obligations repeatedly map to non-core paths (ABI wrappers, tests, or unrelated modules) instead of implementation-critical code paths (`poc5/examples/qualitative_validation_transcript.md:137-163`).

The practical consequence is major review overhead: the reviewer has to filter out path noise before judging semantic correctness.

### Concrete Opus failure mode
Opus rows are often functionally correct, but some statements compress important constraints (e.g., missing conditional clauses or reduced bounds coverage), and some location/flow details are partial (`poc5/examples/qualitative_validation_transcript.md:217-233`).

This is a different risk category from Haiku’s noise:
- Haiku risk: irrelevant mappings.
- Opus risk: plausible but incomplete mappings.

Both are trust risks, but they demand different mitigation strategies.

---

## 2) Finding: Obligation Identity Is Not Stable Across Runs

A core operational issue is obligation renumbering and statement drift across reruns.

Evidence:
- explicit note in qualitative evaluation (`poc5/docs/QUALITATIVE_EVALUATION.md:26`, `:34`),
- transcript-level alignment by statement similarity (`poc5/examples/qualitative_validation_transcript.md:62`, `:275`),
- comparison artifacts requiring semantic matching (`poc4_7/notes/generated/20260129_125052/phase0A_runs/20260129_125052/phase1A_runs/20260129_125145/phase1B_runs/20260129_125500/phase2A_runs/20260129_125803/phase2B_runs/20260129_130116/old_vs_new_qualitative_compare.csv`).

Implication:

> Row-by-row ID comparison is not a valid evaluation method.

If a team evaluates stability or regression by ID equality, it will overestimate disagreement and misclassify drift.

This is why the essay’s scoring sample is keyed to adjudicated obligation entries, not ID continuity assumptions.

---

## 3) Finding: Completeness Metrics Can Mask Correctness Failures

Many run summaries show high population percentages across CSV fields (locations, flows, gaps). That is useful process telemetry, but weak quality evidence.

Example of high completion:
- `poc5/examples/workflow_runs/21571909617/verification-report-7702/summary.md:51-62`

Contrasting quality caveat from spot-check evidence:
- substantial client-location mismatch and noise can coexist with fully populated rows (`poc5/examples/qualitative_validation_transcript.md:132-169`).

This contradiction is formally tracked as:
- `CTR-005` in `docs/evaluations/contradictions.csv`.

Practical rule:

> Treat completion as a process health metric, never as a correctness metric.

Without that rule, teams drift into false confidence because tables "look complete."

---

## 4) Finding: Some Obligations Are Semantically Disputed, Not Just Technically Hard

EIP1559-OBL-030 is the clearest case.

Observed pattern:
- extracted and treated as a normal obligation in runs,
- later flagged as questionable against fork-block behavior in the spec,
- remains unresolved without explicit adjudication.

Evidence:
- `poc5/docs/QUALITATIVE_EVALUATION.md:40-43`
- `poc5/examples/qualitative_validation_transcript.md:246-253`
- `poc5/examples/qualitative_validation_transcript.md:307-317`

In the scored sample, this is labeled `disputed`, not forced into `valid/invalid` simplification.

That distinction is essential. A disputed requirement can produce a coherent mapping narrative while still being semantically ungrounded.

This is a trustworthiness issue, not merely a retrieval issue.

---

## 5) Finding: Environment Context Can Flip the Narrative

Two EIP-7702 workflow runs illustrate this clearly.

- One run reports missing support in geth context.
- Another run is effectively clean with no actionable findings.

Relevant artifacts:
- `poc5/examples/workflow_runs/21570420032/verification-report-7702/summary.md`
- `poc5/examples/workflow_runs/21571909617/verification-report-7702/summary.md`
- contextual interpretation note: `poc5/examples/README.md:30-35`

Tracked as:
- `CTR-004` in `docs/evaluations/contradictions.csv`.

Implication:

> Model-output interpretation without environment metadata is structurally unsafe.

Any serious reporting must include client ref, fork context, and run metadata alongside findings.

---

## 6) Finding: "Low Gap Count" Is Not Equivalent to "Low Error"

In noisy runs, explicit gap columns can remain sparsely populated even while location quality is poor.

This is not necessarily bad faith by the model; it is a schema/behavior mismatch:
- the pipeline can output plausible rows with weak mappings,
- but explicit gap fields may not be triggered proportionally.

Tracked contradiction:
- `CTR-002` in `docs/evaluations/contradictions.csv`.

Operational result:

> Gap-column counts should be interpreted as model-reported concerns, not ground-truth error rates.

This is one reason the essay uses row-level adjudicated scoring instead of relying on gap counters.

---

## 7) Cross-Finding Synthesis: The Bottleneck Is Adjudication Load

Putting the findings together:

1. Models produce materially different error profiles.
2. IDs are unstable across reruns.
3. Completion telemetry overstates trust.
4. Some obligations remain semantically disputed.
5. Environment context changes conclusions.

The shared effect is not "the model failed to write text."

The shared effect is that reviewers must spend significant effort determining what to trust.

That is the trustworthiness bottleneck.

It explains why improving phase structure and artifact traceability produced practical value even when correctness was not fully solved.

---

## 8) What These Findings Do Not Prove

This section intentionally does **not** prove:

1. Formal system-wide precision/recall/F1.
2. A hard architecture ceiling.
3. Generalized model ranking independent of EIP or environment.
4. Universal conclusions about all LLM code-analysis tools.

Those would require larger adjudicated datasets and standardized benchmark procedures.

What this section does provide is strong directional evidence for workflow design priorities in the current repository context.

---

## 9) Practical Implication for Builders (Immediate)

If you are building similar systems today, the highest-leverage moves are:

1. enforce source hierarchy,
2. track contradictions explicitly,
3. score obligation samples with a transparent rubric,
4. treat disputed obligations as first-class outputs,
5. report environment metadata with every finding.

These are trust controls. They reduce downstream review risk even before benchmark-grade accuracy is available.

---

## Transition to Section IV

The next question is not "How do we spin these results positively?"

The next question is:

**What did abandoned approaches teach us about failure visibility, and why did simpler phase-boundary workflows survive in practice?**
