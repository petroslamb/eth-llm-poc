# PoC 4.7

Defaults:
- EIP: **EIP-1559**
- Spec fork: **london** (`specs/execution-specs/src/ethereum/forks/london`)
- Client: **geth** (`clients/execution/geth`)

## Installation (uv + venv)
From the repo root:

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

Run Phase 0A (obligation extraction) from the repo root or pass `--repo-root`:

```sh
poc4_7 --phase 0A --eip 1559 --eip-file specs/EIPs/EIPS/eip-1559.md --model claude-sonnet-4-5 --max-turns 8
```

Run Phase 1A (implementation locations) using the Phase 0A run folder:

```sh
poc4_7 --phase 1A --parent-run poc4_7/notes/generated/<timestamp>/phase0A_runs/<timestamp> --eip 1559 --fork london --model claude-sonnet-4-5 --max-turns 8
```

To rerun a single obligation only:

```sh
poc4_7 --phase 1A --parent-run poc4_7/notes/generated/<timestamp>/phase0A_runs/<timestamp> --eip 1559 --fork london --obligation-id EIP1559-OBL-007 --model claude-sonnet-4-5 --max-turns 8
```

Run Phase 1B (code flow + gaps) using the Phase 1A run folder:

```sh
poc4_7 --phase 1B --parent-run poc4_7/notes/generated/<timestamp>/phase0A_runs/<timestamp>/phase1A_runs/<timestamp> --eip 1559 --model claude-sonnet-4-5 --max-turns 12
```

Run Phase 2A (client locations + code flow) using the Phase 1B run folder:

```sh
poc4_7 --phase 2A --parent-run poc4_7/notes/generated/<timestamp>/phase0A_runs/<timestamp>/phase1A_runs/<timestamp>/phase1B_runs/<timestamp> --eip 1559 --client geth --model claude-sonnet-4-5 --max-turns 20
```

Run Phase 2B (client gap analysis) using the Phase 2A run folder:

```sh
poc4_7 --phase 2B --parent-run poc4_7/notes/generated/<timestamp>/phase0A_runs/<timestamp>/phase1A_runs/<timestamp>/phase1B_runs/<timestamp>/phase2A_runs/<timestamp> --eip 1559 --client geth --model claude-sonnet-4-5 --max-turns 20
```

To target a different fork, pass `--fork` (or override the path with `--spec-root`).

To target a different client, pass `--client` (or override the path with `--client-root`).

To target a non-default client checkout, pass `--client-root` (or legacy `--geth-root`):

```sh
poc4_7 --phase 2A --parent-run poc4_7/notes/generated/<timestamp>/phase0A_runs/<timestamp>/phase1A_runs/<timestamp>/phase1B_runs/<timestamp> --client geth --client-root /path/to/geth
```

Example: non-default EIP, fork, and client

```sh
poc4_7 --phase 0A --eip 4844 --eip-file specs/EIPs/EIPS/eip-4844.md --model claude-sonnet-4-5 --max-turns 8
poc4_7 --phase 1A --parent-run poc4_7/notes/generated/<timestamp>/phase0A_runs/<timestamp> --eip 4844 --fork cancun --model claude-sonnet-4-5 --max-turns 8
poc4_7 --phase 2A --parent-run poc4_7/notes/generated/<timestamp>/phase0A_runs/<timestamp>/phase1A_runs/<timestamp>/phase1B_runs/<timestamp> --eip 4844 --client nethermind --model claude-sonnet-4-5 --max-turns 20
```

## Spec indexing (execution-specs)
Generate the execution-specs EIP <-> fork map and spec index (README + fork `__init__.py` verification):

```sh
poc4_7 index-specs \
  --spec-root specs/execution-specs \
  --spec-readme specs/execution-specs/README.md
```

Outputs are written to `poc4_7/notes/generated/index_runs/<timestamp>/` by default.
The index run includes `eip_fork_map.json`, `spec_index.json`, `spec_index_report.md`, and `run_manifest.json`.
To fail Phase 1A when README and fork `__init__.py` EIP lists diverge, pass `--spec-map-strict` (or set `POC4_7_SPEC_MAP_STRICT=1` or `spec_map_strict: true` in config).

## Run summary report
Generate a summary report for a run root (JSON + Markdown by default):

```sh
poc4_7 report --run-root poc4_7/notes/generated/<timestamp>
```

Outputs `summary.json` and `summary.md` in the run root unless `--output-dir` is provided.

All prompts and outputs are written under `poc4_7/notes/generated/` with nested timestamped run folders.
Each phase now also writes a `run_manifest.json` in its run folder with metadata such as inputs, outputs, and selected client/fork. Example:

```json
{
  "phase": "2A",
  "generated_at": "20250129_153012",
  "input_csv": "poc4_7/notes/generated/20250129_150000/phase0A_runs/20250129_150100/phase1A_runs/20250129_150900/phase1B_runs/20250129_151500/obligations_index.csv",
  "output_csv": "poc4_7/notes/generated/20250129_150000/phase0A_runs/20250129_150100/phase1A_runs/20250129_150900/phase1B_runs/20250129_151500/phase2A_runs/20250129_152200/client_obligations_index.csv",
  "eip_number": "1559",
  "client_name": "geth",
  "client_root": "clients/execution/geth",
  "parent_run": "poc4_7/notes/generated/20250129_150000/phase0A_runs/20250129_150100/phase1A_runs/20250129_150900/phase1B_runs/20250129_151500"
}
```

### Notes
- The CLI runs the Claude agent with tool permissions auto-approved so it can read/write files without interactive prompts.
- Phase requirements (constraint splitting, enforcement hops, location validation) are defined in `poc4_7/PHASE_PLAN.md`.

### Optional config
If `poc4_7/config.yaml` exists, it can set defaults:

```yaml
eip_file: specs/EIPs/EIPS/eip-1559.md
eip: 1559
fork: london
spec_root: specs/execution-specs/src/ethereum/forks/london
model: claude-sonnet-4-5
max_turns: 1
allowed_tools: ["Read", "Write", "Bash", "Grep", "Glob"]
client: geth
client_root: clients/execution/geth
geth_root: clients/execution/geth
```

CLI flags always override config values.
