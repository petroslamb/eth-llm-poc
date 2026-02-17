# Knowledge Gaps Analysis: "The Trustworthiness Gap in LLM Protocol Verification"

## Purpose
This document tracks what must be true for a publication-grade essay that is both persuasive and technically defensible.

The key shift: we are no longer trying to "prove a model ceiling" first. We are trying to prove that **trustworthiness bottlenecks** are visible in the current evidence and actionable with engineering controls.

Status update (2026-02-17):
- Gap 2 (contradiction register) is now implemented in `docs/evaluations/contradictions.csv`.
- Gap 3 (scoring rubric) is now implemented in `docs/evaluations/scoring_rubric.md`.
- Gap 6 (approach decision log) is now implemented in `docs/evaluations/approach_decision_log.csv`.
- Gap 5 (quantified adjudication burden) remains partially open; workload is evidenced, but measured minutes-per-obligation are still limited.
- Run-dependent open items are tracked in `docs/evaluations/future_work.md`.

Traceability note:
- Several sections below preserve original pre-resolution gap statements for audit history.
- Current actionable gaps are the run-dependent items listed in `docs/evaluations/future_work.md`.

Run-dependent priorities:
1. Controlled filter-constrained rerun to upgrade C016.
2. Measured minutes-per-obligation on baseline vs filtered runs to fully close C013.
3. Balanced compare-derived expansion across model families.

---

## Critical Gaps (Must Resolve Before Publication)

### 1. Canonical Evidence Hierarchy (Source-of-Truth Problem)
**What is missing:**
- A formal rule for handling conflicts between raw CSV artifacts, summaries, and narrative README files.

**Why it matters:**
- Current evidence includes contradictory statements (e.g., "full compliance" vs "high noise").
- Without precedence rules, readers can dismiss the essay as cherry-picked.

**Required output:**
- `evidence_hierarchy.md` with explicit precedence:
  1. Raw CSV/manifests/prompts/outputs
  2. Qualitative evaluation reports
  3. Narrative run readmes and retrospective notes

**Effort:** 0.5 day

---

### 2. Contradiction Register (Conflict Resolution Problem)
**What is missing:**
- A single table listing every major contradiction and its resolution status.

**Why it matters:**
- Negative evidence is currently scattered across transcripts and run notes.

**Required output:**
- `contradictions.csv` with columns:
  - `topic`
  - `source_a`
  - `source_b`
  - `conflict_type`
  - `resolution_status`
  - `resolution_note`

**Effort:** 1 day

---

### 3. Reproducible Quality Rubric (Evaluation Problem)
**What is missing:**
- A consistent scoring rubric for obligation-level quality.

**Why it matters:**
- "Looks plausible" is not enough for a top-tier technical essay.

**Required output:**
- Obligation scoring rubric with:
  - statement fidelity (explicit vs inferred)
  - spec location validity
  - client location validity
  - code-flow plausibility
  - evidence sufficiency
- Clear labels: `valid`, `partial`, `invalid`, `disputed`.

**Effort:** 1-2 days

---

### 4. Cross-Run Alignment Method (ID Instability Problem)
**What is missing:**
- A documented method for matching obligations across runs when IDs change.

**Why it matters:**
- Row-by-row comparison by ID produces false disagreements.

**Required output:**
- Alignment methodology note:
  - statement similarity thresholding
  - one-to-one mapping policy
  - ambiguous match handling

**Effort:** 0.5 day

---

### 5. Quantified Adjudication Burden (Operational Reality Problem)
**What is missing:**
- Measurement of review effort required to trust outputs.

**Why it matters:**
- The essay thesis is trustworthiness; adjudication burden is the key operational metric.

**Required output:**
- Sample time-and-effort metrics:
  - minutes per obligation to verify
  - % obligations requiring manual dispute handling
  - model-specific rework burden

**Effort:** 1 day (sample-based)

---

### 6. Negative Results Documentation (Abandonment Problem)
**What is missing:**
- Structured evidence for why specific approaches were abandoned (not just narrative assertions).

**Why it matters:**
- "We abandoned it" without acceptance criteria reads as opinion.

**Required output:**
- Approach decision log:
  - hypothesis
  - experiment setup
  - observed failure mode
  - stop condition
  - retained lessons

**Effort:** 1 day

---

## High-Value Gaps (Materially Improve Quality)

### 7. Cost vs Trustworthiness Analysis
**What is missing:**
- Not just token cost, but **cost per validated obligation**.

**Required output:**
- Compare model runs on:
  - nominal token/call cost
  - manual validation cost
  - total cost-to-trust

**Effort:** 1 day

---

### 8. Environment Sensitivity Framing
**What is missing:**
- Explicit treatment of client ref / fork context as causal variables for outcomes.

**Required output:**
- Environment sensitivity section with run metadata examples.

**Effort:** 0.5 day

---

### 9. Claim Confidence Tags in Draft
**What is missing:**
- Confidence labels on core claims.

**Required output:**
- Every major claim tagged as `high`, `medium`, or `hypothesis` with linked evidence.

**Effort:** 0.5 day

---

## Current Evidence Inventory

### Strong Evidence
- Multi-phase artifact structure and reproducibility scaffolding.
- Cross-model qualitative comparison with concrete failure patterns.
- Documented examples of obligation instability and ambiguous requirements.
- Real workflow runs showing environment-sensitive outcomes.

### Medium Evidence
- Comparative quality differences between Sonnet/Opus/Haiku in sampled runs.
- Cost templates and example usage snapshots.
- Narrative records of abandoned approaches.

### Weak Evidence
- Any strict precision/recall/F1 claim.
- Any hard architecture ceiling claim.
- Any broad prediction about industry standards by fixed year.

---

## Red-Line Rules for the Essay

1. Do not state numeric accuracy claims without a published scoring protocol.
2. Do not use "full compliance" language without obligation-level adjudication evidence.
3. Treat unresolved contradictions as explicit findings, not as footnotes.
4. Distinguish observed evidence from inferred interpretation in every section.
5. Prefer narrow, falsifiable operational claims over sweeping architecture claims.

---

## Minimum Publishable Standard (A-Level)

To publish safely and credibly:
1. Evidence hierarchy document complete.
2. Contradiction register complete for all major claims.
3. At least one scored cross-run sample using a clear rubric.
4. Claim confidence tags added to final draft.
5. Explicit "what this does not prove" section included.

---

## Next Steps

1. Execute items in `docs/evaluations/future_work.md` that require controlled reruns.
2. Promote/demote C013 and C016 after rerun measurements.
3. Keep publish narrative bounded to current non-rerun evidence until those items are complete.
