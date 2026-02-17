# Essays Workspace Guide

## Goal
This directory contains the full essay production package for the trustworthiness thesis:

- main claim: auditability improved faster than correctness in the analyzed LLM-assisted protocol-verification artifacts,
- method: claim-by-claim evidence gating, contradiction tracking, and obligation-level scoring,
- publishing posture: separate current evidence from run-dependent future work.

## Canonical Outputs
1. Canonical research working note: `docs/research_working_note/research_working_note.md`
2. Distribution helper: `docs/research_working_note/research_working_note_bundle.md`
3. Method reference: `docs/research_working_note/essay_methodology.md`

## Current Evidence Snapshot
- Scored rows: 81 (`docs/evaluations/sample_scored_run.csv`)
- Composition: 47 direct-adjudication rows + 34 compare-derived rows
- Metrics summary: `docs/evaluations/metrics_summary.md`

Important boundary:
- Compare-derived rows are medium-confidence proxy evidence for trust-risk and triage, not a replacement for full manual adjudication.

## Read Paths By Objective

### Share now
1. `docs/research_working_note/research_working_note.md`
2. `docs/research_working_note/research_working_note_bundle.md`
3. `docs/evaluations/metrics_summary.md` (final numeric verification)

### Audit claim rigor
1. `docs/evaluations/claim_audit.md`
2. `docs/evaluations/evidence_ledger.md`
3. `docs/evaluations/contradictions.csv`
4. `docs/evaluations/scoring_rubric.md`
5. `docs/evaluations/sample_scored_run.csv`

### Understand how this was produced
1. `docs/research_working_note/essay_methodology.md`
2. `docs/evaluations/sources.md`
3. `docs/research_working_note/full_draft_research_working_note.md`

### Extend evidence quality
1. `docs/evaluations/future_work.md`
2. `docs/evaluations/path_filter_experiment.md`
3. `docs/evaluations/approach_decision_log.csv`

## Artifact Map

### Narrative files
- `docs/research_working_note/research_working_note.md`: final reader-facing research working note (canonical)
- `docs/research_working_note/full_draft_research_working_note.md`: full technical merged draft
- `docs/research_working_note/draft_section_*.md`: section-level working drafts
- `docs/research_working_note/outline.md`: early structure and argument planning

### Evidence and quality controls
- `docs/evaluations/evidence_ledger.md`: claim registry (C001+), confidence, counterevidence
- `docs/evaluations/claim_audit.md`: mapping from draft claims to ledger IDs
- `docs/evaluations/contradictions.csv`: explicit conflict register and resolutions
- `docs/evaluations/scoring_rubric.md`: obligation scoring dimensions and labels
- `docs/evaluations/sample_scored_run.csv`: scored obligation dataset
- `docs/evaluations/metrics_summary.md`: computed summaries and limits
- `docs/evaluations/sources.md`: source hierarchy and citation map

### Operational/postmortem artifacts
- `docs/evaluations/approach_decision_log.csv`: normalized abandonment/selection rationale
- `docs/evaluations/path_filter_experiment.md`: deterministic path-gating triage experiment
- `docs/evaluations/future_work.md`: run-dependent items deferred from current claims
- `docs/evaluations/knowledge_gaps.md`: gap inventory and status notes

### Packaging/meta
- `docs/research_working_note/research_working_note_bundle.md`: titles, proof-pack links, distribution checklist
- `docs/research_working_note/essay_methodology.md`: step-by-step process used to produce this package

## Update Protocol (when making changes)
1. If scored rows change, update `docs/evaluations/sample_scored_run.csv` first.
2. Recompute and update `docs/evaluations/metrics_summary.md`.
3. Sync claim implications in `docs/evaluations/evidence_ledger.md`.
4. Re-run coverage checks in `docs/evaluations/claim_audit.md`.
5. Update narrative files (`docs/research_working_note/research_working_note.md`, optionally `docs/research_working_note/full_draft_research_working_note.md`).
6. Keep run-dependent claims in `docs/evaluations/future_work.md` until new-run evidence exists.

## Non-Negotiables
1. Do not add precision/recall/F1 claims without benchmark-grade ground truth.
2. Do not treat completion percentages as correctness evidence.
3. Keep disputed obligations explicitly labeled.
4. Keep a strict separation between current evidence and future-work hypotheses.
