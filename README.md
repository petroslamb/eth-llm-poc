# eip-verify

LLM-powered verification of EIP obligations against execution-specs and client implementations.

## Installation

```sh
pip install -e .
```

Or with uv:

```sh
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

Set your Anthropic API key:

```sh
export ANTHROPIC_API_KEY="..."
```

### Configuration

The tool supports configuration via CLI arguments, a YAML config file, and environment variables.

**Precedence (Highest to Lowest):**
1. CLI Arguments (`--llm-mode fake`)
2. Config File (`config.yaml` in CWD, or via `--config`)
3. Environment Variables
4. Default Values

**Environment Variables:**
*   `ANTHROPIC_API_KEY`: **Required** for live mode.
*   `EIP_VERIFY_LLM_MODE`: Set default mode (`live` or `fake`).
*   `EIP_VERIFY_RECORD_LLM_CALLS`: Set to `true` to record interactions.

**Config File:**
A template is available at `example_config.yaml`. Copy it to `config.yaml` to use:

```sh
cp example_config.yaml config.yaml
# Edit config.yaml...
eip-verify pipeline ...
```

Or pass it explicitly:

```sh
eip-verify pipeline --config ./my-config.yaml ...
```

### Commands

```
eip-verify <command> [options]

Commands:
  extract         Extract obligations from EIP markdown
  locate-spec     Find implementation locations in execution-specs
  analyze-spec    Analyze code flow and gaps in spec
  locate-client   Find implementation locations in client repo
  analyze-client  Analyze code flow and gaps in client
  index-specs     Generate spec index and EIP→fork mapping
  report          Generate run summary report
```

### Full Pipeline (Local or CI)

Run the entire verification process in one command:

```sh
eip-verify pipeline \
  --eip 1559 \
  --phases "extract,locate-spec,analyze-spec,locate-client,analyze-client" \
  --spec-repo ~/specs/execution-specs \
  --client-repo ~/clients/geth \
  --model claude-sonnet-4-5
```

### Manual Steps (Subcommands)

### Fake mode (no LLM calls)

```sh
eip-verify extract \
  --eip-file /path/to/eip-1559.md \
  --spec-repo /path/to/execution-specs \
  --llm-mode fake
```

### Spec indexing

```sh
eip-verify index-specs \
  --spec-repo /path/to/execution-specs \
  --output-dir ./index-output
```

### Run summary

```sh
eip-verify report --run-root ./runs/<timestamp>
```

## Reusable CI Workflow

Use from another repo:

```yaml
name: Run eip-verify

on:
  workflow_dispatch:

jobs:
  verify:
    uses: petroslamb/eth-llm-poc/.github/workflows/ci.yml@main
    with:
      eip: "7702"
      fork: "prague"
      client: "geth"
      model: "claude-sonnet-4-5"
      phases: "analyze-client"
      max_turns: "20"
    secrets:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## GitHub Actions Manual Triggers

This repository includes two manual workflows for running verification on-demand:

### 1. Manual Run (`manual_run.yml`)
Run verification for a single EIP.
*   **Trigger**: Actions tab -> "Manual Run" -> "Run workflow"
*   **Inputs**: EIP number, fork, client, etc.

### 2. Manual Run (Batch) (`manual_run_batch.yml`)
Run verification for multiple EIPs or an entire fork in parallel.
*   **Trigger**: Actions tab -> "Manual Run (Batch)"
*   **Inputs**:
    *   `eip`: Comma-separated list (e.g., `1559, 2930`). **Leave empty to run ALL EIPs in the fork.**
    *   `fork`: The fork to use if `eip` is empty (e.g., `london`).
*   **Output**: Produces a separate artifact (`verification-report-<EIP>`) for each EIP.

## Tests

```sh
pip install -e ".[test]"
pytest -q
```
