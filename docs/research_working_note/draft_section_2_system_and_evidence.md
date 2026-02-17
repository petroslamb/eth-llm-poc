# II. System and Evidence Rules

The first section reframed the problem: this is a trustworthiness problem before it is a capability problem.

To make that argument defensible, we need strict evidence discipline. Without it, the same repository can support opposite narratives.

This section defines the system under study, the source-of-truth hierarchy, and the claim-admission rules used in the rest of the essay.

---

## 1) System Under Study (Operational Scope)

The implementation analyzed here is the PoC pipeline packaged in PoC 5, with the phase chain:

`extract -> locate-spec -> analyze-spec -> locate-client -> analyze-client`

Reference points:
- `poc5/docs/POC_IMPLEMENTATION_SPEC.md:58`
- `poc5/docs/POC_IMPLEMENTATION_SPEC.md:62`
- `poc5/docs/POC_IMPLEMENTATION_SPEC.md:67`

The pipeline emits structured artifacts (CSV, prompts, raw model output, summaries), and those artifacts are the primary evidence substrate for this essay.

Why this matters: when claims are contested, structured artifacts let us inspect the exact row, path, and rationale instead of relying on memory or polished summaries.

---

## 2) Evidence Hierarchy (Canonical)

The essay uses a strict three-tier hierarchy.

### Tier 1 (Primary)
Raw phase artifacts:
- per-phase CSV outputs,
- run manifests,
- phase prompts and model outputs.

Example references:
- `poc5/examples/runs/20260129_133849/phase0A_runs/20260129_133849/phase1A_runs/20260129_134012/phase1B_runs/20260129_134324/phase2A_runs/20260129_134855/phase2B_runs/20260129_135408/client_obligations_index.csv`
- `poc5/examples/workflow_runs/21571909617/verification-report-7702/summary.md` (for run-level structure and latest CSV snapshot context)

### Tier 2 (Supporting)
Evaluation and validation documents that summarize artifact-level findings:
- `poc5/docs/QUALITATIVE_EVALUATION.md`
- `poc5/examples/qualitative_validation_transcript.md`

### Tier 3 (Narrative)
Retrospective/narrative readmes and summaries:
- run README files,
- proposal prose summaries.

Tier 3 is useful context, but not final authority when it conflicts with Tier 1/2 evidence.

This hierarchy is now captured explicitly in:
- `docs/evaluations/sources.md`
- `docs/evaluations/evidence_ledger.md`

---

## 3) Why Hierarchy Is Necessary: Contradictions Are Real

The current corpus contains direct contradictions.

Representative examples (from `docs/evaluations/contradictions.csv`):

1. **Haiku quality contradiction (CTR-001)**
- One source claims full compliance for the run.
- Another source documents high-noise mapping behavior and unrelated client locations.

2. **Gap-count contradiction (CTR-002)**
- Sparse explicit gap flags in CSV columns can coexist with low-quality location mapping in spot-checks.

3. **OBL-030 status contradiction (CTR-003)**
- Appears as a normal obligation in outputs.
- Later treated as questionable/disputed relative to spec support.

4. **EIP-7702 interpretation contradiction (CTR-004)**
- One workflow report says "not implemented".
- Another run is effectively clean.
- Resolution requires environment metadata (client ref/context), not model mythology.

The key outcome is procedural:

> A verification essay must include contradiction handling by design, not as damage control.

---

## 4) Claim Admission Rules

Every strong claim in this essay must satisfy all of the following:

1. Link to at least one Tier-1 or Tier-2 artifact.
2. Include counterevidence when present.
3. Carry a confidence level (`high`, `medium`, `hypothesis`).
4. Avoid converting qualitative findings into numeric claims unless method and dataset are explicit.

These rules are enforced through:
- `docs/evaluations/evidence_ledger.md` (claim registry C001+)
- `docs/evaluations/contradictions.csv` (conflict registry)

This structure prevents accidental overclaiming such as:
- using completion metrics as correctness metrics,
- using narrative confidence as validation evidence,
- using sampled observations as population-level benchmarks.

---

## 5) Quality Scoring Protocol for Obligation-Level Findings

To avoid subjective grading, this essay uses a fixed rubric:
- `docs/evaluations/scoring_rubric.md`

Dimensions (0/1/2 each):
1. `statement_fidelity`
2. `spec_location_validity`
3. `client_location_validity`
4. `flow_plausibility`
5. `evidence_sufficiency`

Output labels:
- `valid`
- `partial`
- `invalid`
- `disputed`

Crucial design choice: `disputed` is semantic and can override a high numeric total in narrative interpretation. This is important for obligations like EIP1559-OBL-030, where mapping mechanics may look coherent while the requirement itself is contested.

---

## 6) Sample Metrics (What We Can Claim Now)

From the scored sample:
- `docs/evaluations/sample_scored_run.csv`
- `docs/evaluations/metrics_summary.md`

Current sample facts:
- 81 scored obligations (47 direct-adjudication + 34 compare-derived),
- Haiku sample average: 3.5/10 in expanded view (5.0/10 in direct-adjudication subset),
- Opus sample average: 9.4/10,
- Sonnet sample average: 9.0/10,
- three disputed obligations retained explicitly.

These metrics support directional statements about model error profiles in sampled evidence.

They do **not** support formal precision/recall/F1 claims for the system overall. That remains future work and is already marked as a gap in:
- `poc5/docs/QUALITATIVE_EVALUATION.md:14`
- `docs/evaluations/knowledge_gaps.md`

---

## 7) What Counts as "Supported" vs "Inferred"

### Supported (acceptable as core evidence)
- Model-specific qualitative error patterns documented across multiple artifacts.
- Obligation ID instability and need for statement-level alignment.
- Environment-sensitive interpretation of run outcomes.
- Completeness-vs-correctness divergence.

### Inferred (must be labeled as interpretation)
- Cross-approach comparative superiority without uniform benchmark protocol.
- Broad architectural limits from current sample size.
- Forecasts on industry adoption timelines.

This distinction matters because the essay’s credibility depends on visible epistemic boundaries, not rhetorical confidence.

---

## 8) Why This Section Is the Real Backbone

A common technical essay pattern is: narrative first, evidence later. That pattern fails here because the evidence itself is internally heterogeneous and occasionally conflicting.

The trustworthiness angle only works if the reader can audit the audit.

That is why this section front-loads:
- artifact precedence,
- contradiction resolution,
- score protocol,
- claim gating.

With that foundation in place, the next section can present findings without slipping into the exact overconfidence behavior this essay criticizes.

---

## Transition to Section III

Now that the evidence rules are explicit, we can ask a narrower and more useful question:

**Given these rules, what do the runs actually show about model behavior, obligation stability, and verification risk?**
