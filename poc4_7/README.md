# PoC 4.7

Standalone verification tool for EIP obligations against execution specs and client implementations.

## Installation (uv + venv)

```sh
cd poc4_7
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```

To use a standard venv instead of uv:

```sh
cd poc4_7
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

Set your Anthropic API key before running:

```sh
export ANTHROPIC_API_KEY="..."
```

For non-interactive runs, set Claude to write config/session files inside the repo:

```sh
export HOME="$(pwd)"
export XDG_CONFIG_HOME="$(pwd)"
export CLAUDE_CONFIG_DIR="$(pwd)/.claude"
```

Recommended model + turns:
- Phase 0A: `--model claude-sonnet-4-5 --max-turns 8`
- Phase 1A: `--model claude-sonnet-4-5 --max-turns 8`
- Phase 1B: `--model claude-sonnet-4-5 --max-turns 12`
- Phase 2A: `--model claude-sonnet-4-5 --max-turns 20`
- Phase 2B: `--model claude-sonnet-4-5 --max-turns 20`

### Phase 0A: Extract obligations from EIP

```sh
poc4_7 --phase 0A \
  --eip-file /path/to/eip-1559.md \
  --spec-repo /path/to/execution-specs \
  --output-dir ./runs \
  --model claude-sonnet-4-5 --max-turns 8
```

Required args: `--eip-file`, `--spec-repo`
Optional: `--eip` (inferred from filename), `--output-dir` (defaults to `./poc4_7_runs/<timestamp>`)

### Phase 1A: Find spec locations

```sh
poc4_7 --phase 1A \
  --parent-run ./runs/phase0A_runs/<timestamp> \
  --spec-repo /path/to/execution-specs \
  --fork london \
  --model claude-sonnet-4-5 --max-turns 8
```

Required args: `--parent-run`, `--spec-repo`
Optional: `--fork` (defaults to `london`), `--obligation-id` (process single obligation)

### Phase 1B: Analyze code flow

```sh
poc4_7 --phase 1B \
  --parent-run ./runs/phase0A_runs/.../phase1A_runs/<timestamp> \
  --model claude-sonnet-4-5 --max-turns 12
```

Required args: `--parent-run`
Optional: `--spec-repo` (inferred from parent manifest), `--obligation-id`

### Phase 2A: Find client locations

```sh
poc4_7 --phase 2A \
  --parent-run ./runs/.../phase1B_runs/<timestamp> \
  --client-repo /path/to/geth \
  --model claude-sonnet-4-5 --max-turns 20
```

Required args: `--parent-run`, `--client-repo`
Optional: `--obligation-id`

### Phase 2B: Identify client gaps

```sh
poc4_7 --phase 2B \
  --parent-run ./runs/.../phase2A_runs/<timestamp> \
  --client-repo /path/to/geth \
  --model claude-sonnet-4-5 --max-turns 20
```

Required args: `--parent-run`, `--client-repo`
Optional: `--obligation-id`

### Example: Full pipeline

```sh
# Phase 0A
poc4_7 --phase 0A \
  --eip-file ~/specs/EIPs/EIPS/eip-1559.md \
  --spec-repo ~/specs/execution-specs \
  --output-dir ./my-run \
  --model claude-sonnet-4-5 --max-turns 8

# Phase 1A (using Phase 0A output)
poc4_7 --phase 1A \
  --parent-run ./my-run/phase0A_runs/<timestamp> \
  --spec-repo ~/specs/execution-specs \
  --fork london \
  --model claude-sonnet-4-5 --max-turns 8

# Phase 1B (using Phase 1A output)
poc4_7 --phase 1B \
  --parent-run ./my-run/phase0A_runs/.../phase1A_runs/<timestamp> \
  --model claude-sonnet-4-5 --max-turns 12

# Phase 2A (using Phase 1B output)
poc4_7 --phase 2A \
  --parent-run ./my-run/.../phase1B_runs/<timestamp> \
  --client-repo ~/clients/geth \
  --model claude-sonnet-4-5 --max-turns 20

# Phase 2B (using Phase 2A output)
poc4_7 --phase 2B \
  --parent-run ./my-run/.../phase2A_runs/<timestamp> \
  --client-repo ~/clients/geth \
  --model claude-sonnet-4-5 --max-turns 20
```

### Fake mode (no LLM calls)

To run without a real LLM call, set `--llm-mode fake`. Fake mode uses a packaged fake agent to emit placeholder output and CSVs.

```sh
poc4_7 --phase 0A \
  --eip-file /path/to/eip-1559.md \
  --spec-repo /path/to/execution-specs \
  --llm-mode fake
```

## Spec indexing (execution-specs)

Generate the execution-specs EIP <-> fork map and spec index:

```sh
poc4_7 index-specs \
  --spec-repo /path/to/execution-specs \
  --output-dir ./index-output
```

Required args: `--spec-repo`, `--output-dir`

Outputs: `eip_fork_map.json`, `spec_index.json`, `spec_index_report.md`, `run_manifest.json`

## Run summary report

Generate a summary report for a run root:

```sh
poc4_7 report --run-root ./my-run
```

Outputs `summary.json` and `summary.md` in the run root unless `--output-dir` is provided.

## Run manifest

Each phase writes a `run_manifest.json` in its run folder with metadata:

```json
{
  "phase": "2A",
  "generated_at": "20250129_153012",
  "input_csv": "...",
  "output_csv": "...",
  "eip_number": "1559",
  "client_name": "geth",
  "client_root": "/path/to/geth",
  "cwd": "/path/to/geth",
  "parent_run": "..."
}
```

## Notes

- The CLI runs the Claude agent with tool permissions auto-approved so it can read/write files without interactive prompts.
- Set `--llm-mode fake` to skip real LLM calls and record prompt/options metadata.
- Phase requirements are defined in `poc4_7/PHASE_PLAN.md`.

## Optional config

If `config.yaml` exists in the current directory, it can set defaults:

```yaml
eip_file: /path/to/eip-1559.md
eip: 1559
fork: london
spec_repo: /path/to/execution-specs
client_repo: /path/to/geth
output_dir: ./runs
model: claude-sonnet-4-5
max_turns: 1
allowed_tools: ["Read", "Write", "Bash", "Grep", "Glob"]
llm_mode: live
record_llm_calls: false
```

CLI flags always override config values.

## Tests

Run tests from the package root:

```bash
python -m pip install -e ".[test]"
pytest -q
```
