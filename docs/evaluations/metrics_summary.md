# Metrics Summary (Expanded Scored Sample)

## Scope
This summary is computed from:
- `docs/evaluations/sample_scored_run.csv`
- Scoring rules in `docs/evaluations/scoring_rubric.md`

Dataset composition:
- Total scored obligations: **81**
- Direct adjudication rows (transcript/code spot-check evidence): **47**
- Compare-derived rows (cross-run qualitative compare scoring): **34**

## Overall Distribution (All 81 Rows)
- `valid`: 29
- `partial`: 10
- `invalid`: 39
- `disputed`: 3
- Overall average score: **5.5 / 10**

## By Model

### `claude-haiku-4-5`
- Rows: **49**
- Average score: **3.5 / 10**
- Labels: `{ valid: 2, partial: 7, invalid: 39, disputed: 1 }`

### `claude-opus-4-5`
- Rows: **20**
- Average score: **9.4 / 10**
- Labels: `{ valid: 16, partial: 3, invalid: 0, disputed: 1 }`

### `claude-sonnet-4-5`
- Rows: **12**
- Average score: **9.0 / 10**
- Labels: `{ valid: 11, partial: 0, invalid: 0, disputed: 1 }`

## By Model + EIP
- `claude-haiku-4-5` / EIP-1559: 49 rows, avg 3.5, labels `{valid:2, partial:7, invalid:39, disputed:1}`
- `claude-opus-4-5` / EIP-1559: 15 rows, avg 9.2, labels `{valid:11, partial:3, disputed:1}`
- `claude-opus-4-5` / EIP-2930: 5 rows, avg 10.0, labels `{valid:5}`
- `claude-sonnet-4-5` / EIP-1559: 12 rows, avg 9.0, labels `{valid:11, disputed:1}`

## Compare-Block vs Direct-Adjudication Split
- Compare-derived block (`run_id=20260129_125052_compare`): 34 rows, avg 2.8, labels `{invalid:33, disputed:1}`
- Non-compare rows: 47 rows, avg 7.9, labels `{valid:29, partial:10, invalid:6, disputed:2}`

Interpretation: the compare-derived block is intentionally conservative and should be read as a trust-risk signal, not as a direct substitute for row-level manual validation.

## Adjudication-Burden Proxies (Current Data, No New Run)
- Direct-adjudication rows requiring manual follow-up (`partial` + `invalid` + `disputed`): **18 / 47** (**38.3%**)
- Expanded dataset rows requiring manual follow-up: **52 / 81** (**64.2%**)

Direct-adjudication follow-up rate by model:
- `claude-haiku-4-5`: 13/15 (86.7%)
- `claude-opus-4-5`: 4/20 (20.0%)
- `claude-sonnet-4-5`: 1/12 (8.3%)

These are workload proxies (how often review escalation is needed), not measured minutes-per-obligation.

## Immediate Interpretation
1. The expanded sample strengthens the directional finding that error profiles differ materially across models.
2. Disputed obligations remain present even in high-scoring model outputs.
3. Cross-run compare scoring surfaces substantial mapping instability/noise and increases adjudication burden signals.

## Important Limits
1. This is still not a benchmark-grade random sample.
2. Compare-derived rows are medium-confidence proxy scoring from cross-run similarity/overlap evidence, not full manual row validation.
3. Model totals are not perfectly apples-to-apples because the compare-derived expansion currently targets the Haiku run family.
4. No precision/recall/F1 claim should be derived from this summary.
5. Measured minutes-per-obligation require a controlled rerun/instrumented review protocol (tracked in `docs/evaluations/future_work.md`).

## Reproducibility Note
All totals can be recomputed directly from `docs/evaluations/sample_scored_run.csv` using `total_score`, `label`, `model`, `eip`, and `run_id`.
