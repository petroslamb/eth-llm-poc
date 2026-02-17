# VI. Practical Framework for Builders

This section turns the trustworthiness pattern into an implementation playbook.

It assumes a team needs useful outputs now, cannot wait for ideal benchmarks, and still must avoid overclaiming.

---

## 1) KPI Shift: Measure Cost-to-Trust, Not Cost-Per-Run

Most teams track token spend and runtime. Those are necessary, but not sufficient.

For verification workflows, the dominant hidden cost is adjudication effort.

Track at minimum:
1. minutes-to-validate per obligation,
2. % obligations marked `partial/invalid/disputed`,
3. contradiction rate per run,
4. rerun drift requiring remapping.

Why: a cheap run with heavy review burden is operationally expensive.

---

## 2) Release Readiness Gates

Before publishing any external claim, require all gates:

### Gate A — Evidence Gate
- Claim appears in `evidence_ledger.md`.
- Tier and confidence are explicitly set.

### Gate B — Contradiction Gate
- Any conflicting source is present in `contradictions.csv`.
- Resolution status is not implicit.

### Gate C — Scoring Gate
- Relevant obligation sample has rubric scores.
- Label distribution is reported with caveats.

### Gate D — Metadata Gate
- Environment context (fork/client ref/run context) is attached.

No gate, no strong claim.

---

## 3) Model Selection Policy (Operational, Not Ideological)

Do not choose models by narrative reputation. Choose by observed error profile under your rubric.

In current sample evidence:
- Haiku-like profile: high path-noise risk, heavier reviewer filtering cost.
- Opus-like profile: stronger mapping quality with incompleteness/dispute caveats.

Framework recommendation:
1. Use higher-quality model for high-impact runs.
2. Use lower-cost model only with stronger deterministic guards and stricter path constraints.
3. Publish caveats tied to sampled evidence.

This is consistent with directional findings, without asserting unproven global rankings.

---

## 4) Prompt/Schema Hardening Priorities

Given observed failure modes, prioritize hardening in this order:

1. Client path plausibility constraints
- restrict irrelevant path classes unless explicitly justified.

2. Constraint completeness requirements
- require inclusion of critical qualifiers (bounds, fork-conditional branches).

3. Disputed-obligation handling
- mandate `disputed` status where requirement support is ambiguous.

4. Gap-column semantics
- clarify that gap fields are model-reported concerns, not objective error counters.

Pilot signal: in the compare block (`docs/evaluations/path_filter_experiment.md`), deterministic path gating flagged 23/34 noise-only rows and would have dropped 30/34 rows before deep review.

---

## 5) Reporting Template for Responsible External Communication

Use a fixed report envelope:

1. Scope and environment.
2. Evidence tier used for each major claim.
3. Sample quality metrics.
4. Contradictions and resolution status.
5. What remains unknown.

This template prevents accidental overstatement while preserving practical insight.

---

## 6) 30-Day Improvement Plan (Concrete)

### Week 1
- Expand scored sample from 42 rows to 80+ with same rubric (completed at 81 rows).
- Normalize statement-alignment method for cross-run matching.

### Week 2
- Implement deterministic path filters for known noisy classes.
- Re-score to estimate reduction in `invalid` mappings.

### Week 3
- Add adjudication-time tracking per obligation.
- Build first cost-to-trust chart (not just token spend).

### Week 4
- Publish revised evidence ledger and contradiction register.
- Update external narrative with upgraded confidence tags.

This plan is deliberately modest and auditable.

---

## 7) What Builders Should Promise Today

Reasonable promise:

> "This system accelerates obligation triage and evidence gathering under explicit uncertainty controls."

Unreasonable promise (today):

> "This system autonomously verifies protocol compliance with high confidence."

The difference between those two statements is credibility.

---

## Transition to Section VII

The project’s strongest contribution is not a claim that verification is solved.

It is a practical demonstration that reliability improves when teams optimize for falsifiability and contradiction handling.
