# Path Filter Experiment (Compare Block)

## Goal
Evaluate whether deterministic client-path filters can identify noisy mapping rows before manual adjudication.

## Dataset
- Source: `poc4_7/notes/generated/20260129_125052/phase0A_runs/20260129_125052/phase1A_runs/20260129_125145/phase1B_runs/20260129_125500/phase2A_runs/20260129_125803/phase2B_runs/20260129_130116/old_vs_new_qualitative_compare.csv`
- Rows analyzed: 34
- Unit: `client_locations_new` field per obligation

## Deterministic Rules

### Noise-pattern blocklist (regex contains)
- `/test`
- `/tests`
- `accounts/abi/bind`
- `beacon/engine`
- `ethclient`
- `graphql`
- `rawdb`
- `t8ntool`
- `simulated`

### Core-path allowlist (regex contains)
- `core/state_transition.go`
- `core/vm/instructions.go`
- `core/types/tx_dynamic_fee.go`
- `consensus/misc/eip1559/eip1559.go`
- `consensus/misc/gaslimit.go`
- `core/types/receipt.go`
- `core/types/transaction_signing.go`
- `core/types/transaction.go`

### Gate tested
Keep row only if at least one allowlisted core path is present.

## Results
- Rows containing at least one noise pattern: **23 / 34** (67.6%)
- Rows containing at least one allowlisted core path: **4 / 34** (11.8%)
- Noise-only rows (noise present, no allowlisted core path): **23 / 34** (67.6%)
- Rows dropped by allowlist gate: **30 / 34** (88.2%)
- Rows retained by allowlist gate: **4 / 34** (11.8%)

## Interpretation
1. A deterministic path gate can aggressively flag likely noisy rows before expensive manual review.
2. This gate is high-recall for obvious noise in this compare block, but potentially over-prunes and can drop recoverable rows.
3. The experiment supports filter viability as a **triage control**, not as proof of final correctness improvement.

## Limits
1. This is not a controlled rerun with regenerated model outputs.
2. Pattern lists are hand-selected and may embed bias.
3. Results are specific to this compare block and should not be generalized without rerun validation.

## Suggested Follow-up
Run one controlled rerun with filter constraints enabled and compare:
- invalid/disputed share,
- reviewer minutes per obligation,
- false-negative rate on known-valid rows.

Run-dependent follow-up tracking is maintained in `docs/evaluations/future_work.md`.
