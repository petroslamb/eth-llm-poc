# Example Runs: Model Mapping

This folder stores example run artifacts keyed by timestamp. The model used for each run can be inferred from the
qualitative validation transcript. Validation was performed with gtp-5.2-codex (high thinking) on codex-cli to reduce Anthropic model bias and increase validation diversity:

- 20260128_192948 -> Sonnet
- 20260129_125052 -> Haiku
- 20260129_133849 -> Opus
- 20260129_161814 -> Opus (EIP-2930 Berlin full phase chain)

Source: examples/qualitative_validation_transcript.md

## Workflow Run Notes

The manual workflow run `21570420032` (artifacts in `examples/workflow_runs/21570420032`) targets a single EIP (EIP-7702) against geth. It failed the EIP-7702 client check because it ran against an older geth ref (`v1.13.14`, the default in `.github/workflows/ci.yml` and shown in the Actions log for that run). That tag predates EIP-7702 support in geth (no `SetCodeTxType` in `core/types/transaction.go`, and no `core/types/tx_setcode.go`), so the pipeline correctly reported the EIP as unimplemented for that client. This is why the run summary says “SetCodeTxType (0x04) and authorization list processing are absent.”

The same workflow run includes Claude usage snapshots for that job (USD, per CSV):

- Cost totals: $4.36 Opus (cache read/write + output) + $0.03 Haiku = $4.39 total.
- Token totals:
  - Opus: 43 input no-cache, 302,527 cache write (5m), 3,301,672 cache read, 32,676 output.
  - Haiku: 16,765 input no-cache, 1,702 output.
- Source files:
  - `examples/workflow_runs/21570420032/claude_api_cost_2026_02_01_to_2026_02_01.csv`
  - `examples/workflow_runs/21570420032/claude_api_tokens_2026_02.csv`
