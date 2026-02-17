# The Trustworthiness Gap in LLM Protocol Verification

**Subtitle:** Why auditability improved faster than correctness in Ethereum EIP mapping

Most LLM verification discussions still ask the wrong first question:

Can the model produce plausible mappings?

In protocol security, that is not the bottleneck.

The bottleneck is trust calibration: which rows are reliable, which are disputed, and which are wrong, under bounded reviewer effort.

That gap between generated output and independently verifiable truth is the trustworthiness gap.

## Evidence Snapshot

This essay uses an 81-row scored sample (`docs/evaluations/sample_scored_run.csv`) with a fixed rubric (`docs/evaluations/scoring_rubric.md`).

### Direct-adjudication block (47 rows)

| Model | Rows | Avg (/10) | valid | partial | invalid | disputed |
|---|---:|---:|---:|---:|---:|---:|
| Haiku | 15 | 5.0 | 2 | 7 | 6 | 0 |
| Opus | 20 | 9.4 | 16 | 3 | 0 | 1 |
| Sonnet | 12 | 9.0 | 11 | 0 | 0 | 1 |

### Expanded block (81 rows)

The expanded view adds 34 medium-confidence compare-derived rows from cross-run qualitative alignment.

| Model | Rows | Avg (/10) | valid | partial | invalid | disputed |
|---|---:|---:|---:|---:|---:|---:|
| Haiku | 49 | 3.5 | 2 | 7 | 39 | 1 |
| Opus | 20 | 9.4 | 16 | 3 | 0 | 1 |
| Sonnet | 12 | 9.0 | 11 | 0 | 0 | 1 |

The headline is not model ranking. The headline is error profile and adjudication cost.

## Methods Note

1. Direct-adjudication rows are based on transcript/code-backed spot checks and are the strongest quality evidence in this pack.
2. Compare-derived rows are medium-confidence proxy scoring from cross-run similarity/overlap artifacts and are intentionally conservative.
3. Compare-derived rows are useful for trust-risk detection and triage planning, but they are not a replacement for full manual adjudication.

## What Failed First

### 1) Evidence governance failed before generation failed

The same repository can produce polished but conflicting narratives. Without explicit source hierarchy and contradiction handling, teams can select whichever narrative sounds best.

### 2) Model differences are mainly error-profile differences

In this corpus:
- Haiku-like behavior shows high client-location noise and high invalid share in the expanded sample.
- Opus/Sonnet-like behavior is materially stronger, but still not dispute-free.

### 3) ID stability is weak across reruns

Obligation IDs drift. Row-by-row ID comparison is not a valid regression method.

### 4) Completeness can mask correctness failure

High field-population percentages can coexist with wrong mappings. "Row populated" is process telemetry, not correctness evidence.

### 5) Some obligations are semantically disputed

OBL-030 remains the canonical case where mapping mechanics look coherent but requirement validity is still contested.

## Why the Simpler Pattern Survived

Context-heavy guided flows and other exploratory architectures produced useful ideas, but struggled on the operational criterion that matters most here: bounded adjudication cost with clear failure attribution.

The surviving phase-boundary pipeline won on inspectability:
- strict phase separation,
- persistent artifacts,
- replayable lineage,
- explicit contradiction tracking.

This is a reliability story, not an architecture-hype story.

## Practical Pattern

Optimize for falsifiability, not narrative confidence.

Minimum controls:
1. Evidence hierarchy with explicit precedence.
2. Rubric-scored obligation samples.
3. Contradiction register as a required artifact.
4. Claim ledger with confidence tags.
5. Environment metadata attached to every external claim.

## Current Workload Signal (No New Run)

From current scored data:
- 18/47 direct-adjudication rows (38.3%) required manual follow-up (`partial`/`invalid`/`disputed`).
- 52/81 rows (64.2%) require follow-up in the expanded sample.

This supports the adjudication-burden thesis, but it is still a proxy view, not timed review measurement.

## Deferred: Run-Dependent Future Work

The following items require new runs and are deferred to `docs/evaluations/future_work.md`:

1. Controlled baseline vs filter-constrained rerun to test whether path filtering improves final quality (C016).
2. Measured minutes-per-obligation on rerun pairs to fully quantify cost-to-trust (C013).
3. Balanced compare-derived expansion across additional model families.

## What Builders Should Promise Today

Reasonable:

> This system accelerates obligation triage and evidence collection under explicit uncertainty controls.

Not reasonable (yet):

> This system autonomously verifies protocol compliance with high confidence.

## What This Does Not Prove

- system-wide precision/recall/F1,
- universal model ranking across tasks and environments,
- benchmark-grade architecture ceilings,
- autonomous low-risk verification readiness.

## Closing

The strongest progress in this project was methodological: the workflow became better at exposing where it might be wrong.

In protocol security, that is the maturity signal that matters.

## Endnotes

1. Pipeline and phase boundaries: `poc5/docs/POC_IMPLEMENTATION_SPEC.md`
2. Qualitative evaluation and known limits: `poc5/docs/QUALITATIVE_EVALUATION.md`
3. Spot-check transcript and cross-model discussion: `poc5/examples/qualitative_validation_transcript.md`
4. Contradiction register: `docs/evaluations/contradictions.csv`
5. Scoring rubric: `docs/evaluations/scoring_rubric.md`
6. Expanded scored dataset: `docs/evaluations/sample_scored_run.csv`
7. Metrics summary: `docs/evaluations/metrics_summary.md`
8. Evidence ledger: `docs/evaluations/evidence_ledger.md`
9. Approach decision log: `docs/evaluations/approach_decision_log.csv`
10. Path filter experiment: `docs/evaluations/path_filter_experiment.md`
11. Run-dependent future work: `docs/evaluations/future_work.md`
