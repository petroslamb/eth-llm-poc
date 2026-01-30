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

### Example: Full pipeline

```sh
# Extract obligations from EIP
eip-verify extract \
  --eip-file ~/specs/EIPs/EIPS/eip-1559.md \
  --spec-repo ~/specs/execution-specs \
  --model claude-sonnet-4-5 --max-turns 8

# Locate spec implementations (using previous run output)
eip-verify locate-spec \
  --parent-run ./runs/<timestamp>/phase0A_runs/<timestamp> \
  --spec-repo ~/specs/execution-specs \
  --fork london \
  --model claude-sonnet-4-5 --max-turns 8

# Analyze spec code flow
eip-verify analyze-spec \
  --parent-run ./runs/.../phase1A_runs/<timestamp> \
  --model claude-sonnet-4-5 --max-turns 12

# Locate client implementations
eip-verify locate-client \
  --parent-run ./runs/.../phase1B_runs/<timestamp> \
  --client-repo ~/clients/geth \
  --model claude-sonnet-4-5 --max-turns 20

# Analyze client gaps
eip-verify analyze-client \
  --parent-run ./runs/.../phase2A_runs/<timestamp> \
  --client-repo ~/clients/geth \
  --model claude-sonnet-4-5 --max-turns 20
```

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

## Tests

```sh
pip install -e ".[test]"
pytest -q
```
