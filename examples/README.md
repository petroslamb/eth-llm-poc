# Example Runs: Model Mapping

This folder stores example run artifacts keyed by timestamp. The model used for each run on the same eip-1559 in order to validate the results and compare models. Validation was performed with `gtp-5.2-codex (high thinking)` on codex-cli to reduce Anthropic model bias and increase validation diversity:

```
- 20260128_192948 -> Sonnet 4.5
- 20260129_125052 -> Haiku 4.5
- 20260129_133849 -> Opus 4.5
- 20260129_161814 -> Opus 4.5 (EIP-2930 Berlin full phase chain)
```

Source: `examples/qualitative_validation_transcript.md`

## Runtime
The runtime for a single EIP for Opus 4.5 can vary from 10 to 20 minutes.

## Model Performance Observations
- **Claude 4.5 Haiku**: Use of this model resulted in a high rate of false positives; the Geth code analysis was generally beyond its capabilities.
- **Claude 4.5 Sonnet**: Performed well with low false positives. Its output was verbose and descriptive, which aided in understanding the context of certain tasks.
- **Claude 4.5 Opus**: The slight favorite. Like Sonnet, it had low false positives, but its concise and specific output style was marginally better suited for this verification task.

**Evaluation Note**: The evaluation of these runs was conducted using `gpt-5.2-codex (high)` on all findings across EIPs, execution-specs, and the Geth client.

More info in `poc5/docs/QUALITATIVE_VALIDATION.md`

## Workflow Run Notes

### Validation of a missing EIP from Geth

The manual workflow run `21570420032` (artifacts in `examples/workflow_runs/21570420032`) targets a single EIP (EIP-7702) against geth. It failed the EIP-7702 client check because it ran against an older geth ref (`v1.13.14`, as shown in the Actions log for that run). That tag predates EIP-7702 support in geth (no `SetCodeTxType` in `core/types/transaction.go`, and no `core/types/tx_setcode.go`), so the pipeline correctly reported the EIP as unimplemented for that client. This is why the run summary says “SetCodeTxType (0x04) and authorization list processing are absent.”

### Successful EIP-7702 validation (no false positives)

The manual workflow run `21571909617` (artifacts in `examples/workflow_runs/21571909617`) completed the EIP-7702 check against geth with no actionable findings. The only note recorded (EIP7702-OBL-030) was a spec-consistent behavior explanation, so the run is considered clean overall with no false positives.

## Workflow indicative cost

The same workflow run includes Claude usage snapshots for that job (USD, per CSV):

- Cost totals: $4.36 Opus (cache read/write + output) + $0.03 Haiku = $4.39 total.
- Token totals:
  - Opus: 43 input no-cache, 302,527 cache write (5m), 3,301,672 cache read, 32,676 output.
  - Haiku: 16,765 input no-cache, 1,702 output.
- Source files:
  - `examples/workflow_runs/21570420032/claude_api_cost_2026_02_01_to_2026_02_01.csv`
  - `examples/workflow_runs/21570420032/claude_api_tokens_2026_02.csv`
