# V. The Trustworthiness Design Pattern

The postmortem points to a simple conclusion:

A verification pipeline is useful only if it is optimized for falsifiability, not just output generation.

This section defines the pattern that emerges from the current evidence.

---

## 1) Design Objective

Primary objective:

> Minimize false confidence per obligation while keeping review cost bounded.

Secondary objective:
- improve mapping quality over time through iterative scoring and adjudication feedback.

This reverses the common priority stack, where teams optimize first for throughput and apparent coverage.

---

## 2) Pattern Components

### Component A — Atomic phase boundaries
- Keep extract/locate/analyze responsibilities separate.
- Preserve phase-level artifacts for replay.

Evidence anchor:
- `poc5/docs/POC_IMPLEMENTATION_SPEC.md:58-69`

### Component B — Artifact continuity
- Every phase output should be inspectable and linked to the next phase input.
- Missing lineage should be treated as an analysis defect.

### Component C — Explicit uncertainty classes
Use standardized obligation statuses:
- `valid`
- `partial`
- `invalid`
- `disputed`

Rubric reference:
- `docs/evaluations/scoring_rubric.md`

### Component D — Contradiction register
- Conflicting interpretations are not noise; they are first-class data.
- Track, resolve, and publish them.

Reference:
- `docs/evaluations/contradictions.csv`

### Component E — Claim gating
- High-confidence claims require high-tier evidence.
- Hypotheses remain explicitly labeled until promoted by stronger evidence.

Reference:
- `docs/evaluations/evidence_ledger.md`

---

## 3) Core Operating Loop

Use a repeated five-step loop:

1. Run phase pipeline.
2. Score sampled obligations with rubric.
3. Record contradictions and disputed rows.
4. Apply targeted prompt/schema/tooling fixes.
5. Re-score and compare deltas.

This loop converts vague "model tuning" into measurable trust improvements.

---

## 4) Why This Pattern Works in Practice

It aligns directly with observed repository pain points:

1. ID instability -> solved by statement-level alignment and scored adjudication.
2. Completion-vs-correctness confusion -> solved by explicit quality labels and score dimensions.
3. Narrative contradictions -> solved by source hierarchy plus contradiction registry.
4. Environment-sensitive outcomes -> solved by mandatory metadata in interpretation.

This is not a claim of perfection. It is a claim of controllability.

---

## 5) What This Pattern Does Not Solve

1. It does not remove semantic ambiguity in specs.
2. It does not guarantee high correctness from weak models.
3. It does not eliminate human review.
4. It does not produce benchmark-grade metrics automatically.

It is a governance and reliability pattern, not a magic retrieval architecture.

---

## 6) Minimal Adoption Checklist

A team can adopt the pattern with these minimum controls:

1. Evidence hierarchy document.
2. Obligation scoring rubric.
3. Contradiction CSV with resolution fields.
4. Sample-scoring checkpoint in each iteration.
5. Claim ledger tying public statements to artifacts.

Current equivalents in this repo:
- `docs/evaluations/sources.md`
- `docs/evaluations/scoring_rubric.md`
- `docs/evaluations/contradictions.csv`
- `docs/evaluations/sample_scored_run.csv`
- `docs/evaluations/evidence_ledger.md`

---

## Transition to Section VI

A pattern is only useful if builders can operationalize it.

Next: a concrete framework for teams shipping LLM-assisted verification systems under time, cost, and credibility constraints.
