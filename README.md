# eip-verify

LLM-powered verification of EIP obligations against execution-specs and client implementations.

## Installation

## Repository Map

```
/
├── .github/workflows/   # CI/CD definitions (standard & batched phases)
├── docs/                # Project roadmap, implementation specs, and RFP docs
├── src/eip_verify/      # Main Python package
│   ├── agents.py        # LLM agent adapters
│   ├── cli.py           # CLI entrypoint (Fire-based)
│   ├── pipeline.py      # Multi-stage verification orchestrator
│   ├── runner.py        # Phase-specific execution logic
│   ├── spec_index.py    # Execution-spec parsing & fork mapping
│   └── prompts/         # System prompts for each verification phase
├── tests/               # Unit and integration tests
├── example_config.yaml  # Template configuration file
└── pyproject.toml       # Build system & dependency definitions
```

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

The reusable workflow has **no internal defaults**; callers must provide all inputs. If you want this repo’s defaults, call the `resolve_defaults.yml` workflow first and pass its outputs into `ci.yml`.

```yaml
name: Run eip-verify

on:
  workflow_dispatch:

jobs:
  defaults:
    uses: petroslamb/eth-llm-poc/.github/workflows/resolve_defaults.yml@main
    with:
      profile: "single"
      eip: ${{ inputs.eip }}
      fork: ${{ inputs.fork }}
      client: ${{ inputs.client }}
      client_ref: ${{ inputs.client_ref }}
      phases: ${{ inputs.phases }}
      model: ${{ inputs.model }}
      max_turns: ${{ inputs.max_turns }}
      eips_ref: ${{ inputs.eips_ref }}
      execution_specs_ref: ${{ inputs.execution_specs_ref }}
      llm_mode: ${{ inputs.llm_mode }}
      pypi_package: ${{ inputs.pypi_package }}

  verify:
    needs: defaults
    uses: petroslamb/eth-llm-poc/.github/workflows/ci.yml@main
    with:
      eip: ${{ needs.defaults.outputs.eip }}
      fork: ${{ needs.defaults.outputs.fork }}
      client: ${{ needs.defaults.outputs.client }}
      client_ref: ${{ needs.defaults.outputs.client_ref }}
      phases: ${{ needs.defaults.outputs.phases }}
      model: ${{ needs.defaults.outputs.model }}
      max_turns: ${{ needs.defaults.outputs.max_turns }}
      eips_ref: ${{ needs.defaults.outputs.eips_ref }}
      execution_specs_ref: ${{ needs.defaults.outputs.execution_specs_ref }}
      llm_mode: ${{ needs.defaults.outputs.llm_mode }}
      pypi_package: ${{ needs.defaults.outputs.pypi_package }}
    secrets:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## GitHub Actions Manual Triggers

This repository includes two manual workflows for running verification on-demand:

### 1. Manual Run (`manual_run.yml`)
Run verification for a single EIP.
*   **Trigger**: Actions tab -> "Manual Run" -> "Run workflow"
*   **Inputs**: EIP number, fork, client, etc. (leave blank to use defaults from `resolve_defaults.yml`)
*   **UI defaults**: Synced from `resolve_defaults.yml` via `scripts/sync_workflow_defaults.py`.

### 2. Manual Run (Batch) (`manual_run_batch.yml`)
Run verification for multiple EIPs or an entire fork in parallel.
*   **Trigger**: Actions tab -> "Manual Run (Batch)"
*   **Inputs**:
    *   `eip`: Comma-separated list (e.g., `1559, 2930`). **Leave empty to run ALL EIPs in the fork.**
    *   `fork`: The fork to use if `eip` is empty (e.g., `london`).
    *   Other inputs can be left blank to use defaults from `resolve_defaults.yml`.
*   **Output**: Produces a separate artifact (`verification-report-<EIP>`) for each EIP.

## Tests

```sh
pip install -e ".[test]"
pytest -q
```

## Example Runs

Example verification runs are available in `examples/runs`.

**Model Performance Observations:**
- **Claude 4.5 Haiku**: Use of this model resulted in a high rate of false positives; the Geth code analysis was generally beyond its capabilities.
- **Claude 4.5 Sonnet**: Performed well with low false positives. Its output was verbose and descriptive, which aided in understanding the context of certain tasks.
- **Claude 4.5 Opus**: The slight favorite. Like Sonnet, it had low false positives, but its concise and specific output style was marginally better suited for this verification task.

**Evaluation Note**: The evaluation of these runs was conducted using `gpt-5.2-codex` on all findings across EIPs, execution-specs, and the Geth client.
