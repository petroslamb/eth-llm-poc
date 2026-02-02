# Integration Guide (GitHub CI/CD)

This guide explains how to integrate PoC 5 into GitHub Actions using the reusable workflow. Detailed runbook steps are in [docs/POC_IMPLEMENTATION_SPEC.md](../POC_IMPLEMENTATION_SPEC.md).

## Reusable Workflow (workflow_call)

Use the reusable workflow from another repo:

```yaml
name: Verify EIP

on:
  workflow_dispatch:

jobs:
  verify:
    uses: petroslamb/eth-llm-poc/.github/workflows/ci.yml@main
    with:
      eip: "7702"
      fork: "prague"
      client: "geth"
      client_ref: "v1.13.14"
      phases: "extract,locate-spec,analyze-spec,locate-client,analyze-client"
      model: "claude-sonnet-4-5"
      max_turns: "20"
      eips_ref: "master"
      execution_specs_ref: "mainnet"
      llm_mode: "fake"
    secrets:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Workflow Inputs

| Input | Default | Description |
| --- | --- | --- |
| `eip` | `7702` | EIP number to verify |
| `fork` | `prague` | Execution-specs fork |
| `client` | `geth` | Execution client name |
| `client_ref` | (resolved) | Client git ref or tag |
| `phases` | all phases | Comma-separated phase list |
| `model` | `claude-sonnet-4-5` | Claude model |
| `max_turns` | `20` | Max turns per phase |
| `eips_ref` | `master` | EIPs repo ref |
| `execution_specs_ref` | `mainnet` | Execution-specs repo ref |
| `llm_mode` | `fake` | `live` or `fake` |
| `pypi_package` | `.` | Local path or PyPI version |

## Outputs and Artifacts

| Output | Path | Notes |
| --- | --- | --- |
| Run artifacts | `runs/ci_run/` | Uploaded as workflow artifact |
| Summary | `runs/ci_run/summary.md` | Human-readable report |
| Summary JSON | `runs/ci_run/summary.json` | Machine-readable report |

## In-Repo Manual Workflows

For manual runs in this repo, see:
- [.github/workflows/manual_run.yml](../../.github/workflows/manual_run.yml)
- [.github/workflows/manual_run_batch.yml](../../.github/workflows/manual_run_batch.yml)
