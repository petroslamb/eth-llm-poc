# Future Work (Requires New Runs)

This file tracks open items that cannot be completed credibly from the current artifact set alone.

## Run-Dependent Items

1. Controlled path-filter rerun (required for C016)
- Run a baseline and filter-constrained pair under the same EIP/model/config.
- Compare `invalid/disputed` rates and false-negative behavior on known-valid obligations.
- Goal: upgrade C016 in `docs/evaluations/evidence_ledger.md` from hypothesis to supported/contested.

2. Measured adjudication minutes per obligation (required to fully close C013)
- Instrument reviewer time per obligation on both baseline and filter-constrained runs.
- Report median and P75 minutes per obligation by model and by label class.
- Goal: replace qualitative workload narrative with measured cost-to-trust metrics.

3. Balanced compare-derived expansion across models
- Generate equivalent cross-run compare blocks for Opus/Sonnet families (not only Haiku-linked compare expansion).
- Goal: remove asymmetry in expanded-sample model totals.

## Why Deferred

Current repository evidence supports directional trust/risk conclusions and triage-control signals, but does not include controlled rerun measurements for the items above.
