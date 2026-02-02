# eip-verify

LLM-powered traceability and verification of EIP obligations against `execution-specs` and execution client implementations (Geth tested).

## Quick Start

1) Fork the repo and add `ANTHROPIC_API_KEY` to your repo secrets.  
2) Go to Actions → **Manual Run** and click **Run workflow**.  
3) Leave inputs blank to use defaults from `resolve_defaults.yml`.  
4) Switch `llm_mode` from `fake` to `live` if you want real LLM calls.

Expected output (≈10–20 minutes):
- A `verification-report-<EIP>` artifact with a run summary (`summary.md`/`summary.json`).
- A phase-by-phase run directory, culminating in the final CSV of atomic obligations and their mappings.

How it works:
Each phase builds on the previous one: extract EIP obligations, locate them in `execution-specs`, analyze spec code flow/gaps, then repeat the same mapping for the execution client. The final CSV in the last phase is the primary artifact for review and reuse.

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

Example validation runs are available in `examples`. Read the `examples/README.md` for model qualitative comparisons and some initial costs on the best `opus-4.5` model.
