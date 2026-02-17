# Obligation Scoring Rubric (v1)

This rubric is for obligation-level quality scoring in validation samples.

Goal: prevent "looks plausible" judgments from being treated as evidence.

---

## Dimensions and Scale

Each dimension is scored `0`, `1`, or `2`.

### 1) Statement Fidelity (`statement_fidelity`)
- `2`: obligation statement matches source requirement with key constraints intact.
- `1`: mostly right intent, but missing qualifiers or compressed constraints.
- `0`: materially wrong, unsupported, or mismatched requirement.

### 2) Spec Location Validity (`spec_location_validity`)
- `2`: cited spec locations directly implement/enforce the stated obligation.
- `1`: nearby/related location, but indirect or incomplete evidence.
- `0`: cited location does not support the obligation.

### 3) Client Location Validity (`client_location_validity`)
- `2`: cited client locations are implementation-relevant and non-incidental.
- `1`: partially relevant (constants/helpers/tests near logic) but incomplete.
- `0`: unrelated/noisy locations (e.g., ABI wrappers/tests/irrelevant modules).

### 4) Flow Plausibility (`flow_plausibility`)
- `2`: code flow narrative correctly links entrypoint -> enforcement path.
- `1`: partly plausible but skips critical transitions or misplaces checks.
- `0`: flow is unsupported or inconsistent with cited locations.

### 5) Evidence Sufficiency (`evidence_sufficiency`)
- `2`: claim backed by explicit spot-check or direct file-level validation notes.
- `1`: indirect support only (summary-level statement without row detail).
- `0`: no usable evidence for adjudication.

---

## Total Score and Labels

`total_score = sum(5 dimensions)` -> range `0..10`

### Label Rules
- `valid`:
  - total >= 8
  - and both `spec_location_validity >= 1` and `client_location_validity >= 1`
- `partial`:
  - total 5..7
  - or total >=8 with one major incompleteness caveat
- `invalid`:
  - total <= 4
  - or either spec/client location validity = 0 with no compensating evidence
- `disputed`:
  - obligation itself is semantically contested (e.g., requirement may be unsupported)
  - can coexist with any numeric total

`disputed` is a semantic flag and takes precedence in reporting narratives.

---

## Confidence of Score

Score confidence (`confidence`) is separate from quality label.

- `high`: row-level validation with explicit rationale and paths in transcript/artifacts.
- `medium`: derived from summary-level claims with limited row detail.
- `low`: inferred without direct row-level evidence.

---

## Adjudication Procedure

1. Normalize paths first (short `fork.py` vs full fork path).
2. Validate statement against spec text intent.
3. Validate spec location supports statement.
4. Validate client location supports statement.
5. Validate flow narrative consistency.
6. Assign numeric scores + label + confidence.
7. If semantically contested, set label to `disputed` regardless of total.

---

## Known Pitfalls

1. 100% populated CSV fields do not imply correctness.
2. ID equality across runs is unreliable; use statement-similarity alignment.
3. Test/ABI/auxiliary paths can inflate apparent mapping coverage.
4. Summaries may under-report quality issues that appear in row-level spot-checks.

---

## CSV Schema for Scored Samples

Required columns:
- `sample_id`
- `run_id`
- `model`
- `eip`
- `obligation_id`
- `statement_fidelity`
- `spec_location_validity`
- `client_location_validity`
- `flow_plausibility`
- `evidence_sufficiency`
- `total_score`
- `label`
- `confidence`
- `evidence_refs`
- `notes`

---

## Example

- Obligation: `EIP1559-OBL-030` in Opus 1559 run
- Observed: location references exist, but requirement itself appears unsupported by spec
- Typical score: `statement_fidelity=0`, `spec_location_validity=1`, `client_location_validity=1`, `flow_plausibility=1`, `evidence_sufficiency=2`, `total=5`, `label=disputed`
