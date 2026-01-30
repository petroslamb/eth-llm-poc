# PoC 4.7 Implementation Plan (Claude SDK, per-obligation mapping)

This plan implements the workflow in `poc4_7/PHASE_PLAN.md` under the constraints in `poc4_7/README.md`.

## Scope and constraints
- EIP: **selected EIP** (default: 1559).
- Codebase (spec): **execution-specs**, selected fork (default: london).
- Codebase (client): **selected execution client** (default: geth).
- Goal: 100% obligation-to-code mapping with line-level evidence or explicit gap classification.
- Phase 2 expands the mapping to align execution-specs code flow with client code flow per obligation.
- Tooling: **Claude Agent SDK (Python)** via `claude_agent_sdk` (no MCP indirection).

## Repository layout
- `poc4_7/pyproject.toml` (installable package via uv/pip)
- `poc4_7/src/poc4_7/prompts/`
  - `phase0A_obligations.txt` (obligation extraction + indexing)
  - `phase1A_locations.txt` (per-obligation location mapping)
  - `phase1B_codeflow.txt` (code flow + gap analysis)
  - `phase2A_client_locations.txt` (client location + code flow mapping)
  - `phase2B_client_gaps.txt` (client gap analysis)
- `poc4_7/notes/generated/<timestamp>/` (run outputs)
  - `phase0A_runs/<timestamp>/`
  - `phase1A_runs/<timestamp>/`
  - `phase1B_runs/<timestamp>/`
  - `phase2A_runs/<timestamp>/`
  - `phase2B_runs/<timestamp>/`
- `poc4_7/config.yaml` (paths, model, budgets, limits)

## Claude SDK usage (per Context7)
We will use `claude_agent_sdk` with:
- `query()` for stateless, one-shot worker calls.
- `ClaudeAgentOptions` and tool configuration per phase.
- Workers are allowed to use filesystem tools and can write the CSV outputs.

## Phase 0A — Obligation extraction + indexing
**Inputs**
- Selected EIP text from the eips repo (canonical source path defined in config).

**Process**
- Read the selected EIP.
- Split compound obligations into atomic statements.
- Assign stable IDs (`EIP1559-OBL-001`, etc.).
- Tag each obligation with category and enforcement type (if applicable).

**Outputs**
- Write a single CSV to:
  - `notes/generated/<timestamp>/phase0A_runs/<timestamp>/obligations_index.csv`
- Columns (in order):
  - `id`
  - `category`
  - `enforcement_type`
  - `statement`
  - `locations`
  - `code_flow`
  - `obligation_gap`
  - `code_gap`
- Save prompts and raw model output in the same run folder.

## Phase 1A — Per-obligation implementation locations
**Inputs**
- `obligations_index.csv` from Phase 0A.
- Selected fork under `specs/execution-specs/src/ethereum/forks/<fork>`.

**Process**
- For each obligation row:
  - Locate all code paths that implement the obligation.
  - Ensure coverage of all viable paths, not just the most direct one.
- Fill `locations` as a list of references:
  - `[path/file.py:L10-L42, path/other.py:function_name]`.

**Outputs**
- Update the CSV (or write a new version alongside it) under:
  - `notes/generated/<timestamp>/phase0A_runs/<timestamp>/phase1A_runs/<timestamp>/`
- Save prompts and raw model output in the same run folder.

## Phase 1B — Code flow + gap analysis
**Inputs**
- CSV updated by Phase 1A.

**Process**
- For each obligation row:
  - Write end-to-end `code_flow`.
  - Fill `enforcement_type` if missing.
  - Identify and classify gaps:
    - `obligation_gap`: missing or ambiguous spec requirement.
    - `code_gap`: missing or unclear implementation path.

**Outputs**
- Update the CSV (or write a new version alongside it) under:
  - `notes/generated/<timestamp>/phase0A_runs/<timestamp>/phase1A_runs/<timestamp>/phase1B_runs/<timestamp>/`
- Save prompts and raw model output in the same run folder.

## Phase 2A — Client locations + code flow
**Inputs**
- Phase 1B CSV output.
- client codebase under `clients/execution/geth` (or an explicit `--client-repo` path).

**Process**
- Create a new CSV derived from Phase 1B that adds client fields:
  - `client_locations`
  - `client_code_flow`
  - `client_obligation_gap`
  - `client_code_gap`
- For each obligation row:
  - Use targeted searches to find relevant client code:
    - Search for the EIP number (e.g., `4844`, `EIP-4844`) and spec terms.
    - Reuse keywords from `statement` and `code_flow` (function names, field names, validation steps).
  - Expand from initial matches to surrounding code, dependencies, and call sites as needed.
  - Record best-effort `client_locations` and a concise `client_code_flow` describing the client path.
- Only write client fields; do not modify Phase 1B columns.

**Outputs**
- Write a new CSV (do not overwrite Phase 1B output) under:
  - `notes/generated/<timestamp>/phase0A_runs/<timestamp>/phase1A_runs/<timestamp>/phase1B_runs/<timestamp>/phase2A_runs/<timestamp>/client_obligations_index.csv`
- Save prompts and raw model output in the same run folder.

## Phase 2B — Client gap analysis
**Inputs**
- Phase 2A CSV output.

**Process**
- For each obligation row:
  - Re-check `client_locations` and `client_code_flow` for coverage; expand searches if needed.
  - Identify and classify gaps:
    - `client_obligation_gap`: client behavior found that is not represented by the obligation statement(s).
    - `client_code_gap`: missing or unclear client implementation for the obligation statement(s).
  - If additional relevant code is discovered, update `client_locations` and `client_code_flow` as part of the best-effort pass.
- Populate only the client gap columns plus any refined client locations/flow.

**Outputs**
- Write the updated CSV under:
  - `notes/generated/<timestamp>/phase0A_runs/<timestamp>/phase1A_runs/<timestamp>/phase1B_runs/<timestamp>/phase2A_runs/<timestamp>/phase2B_runs/<timestamp>/client_obligations_index.csv`
- Save prompts and raw model output in the same run folder.

## Orchestration (package-first)
Implementation should expose Python entry points inside the package rather than ad-hoc scripts. The orchestrator should:
- Accept flags to run individual phases (`--phase 0A`, `--phase 1A`, `--phase 1B`, `--phase 2A`, `--phase 2B`).
- Support per-obligation reruns (`--obligation-id`).
- Always emit:
  - Prompt file
  - Model output file
  - CSV updates
- Ensure nested run folders so later steps can be rerun without changing earlier outputs.
  - Phase 2A must be nested inside a selected Phase 1B run.
  - Phase 2B must be nested inside a selected Phase 2A run.

## Quality controls
- Deterministic prompts and fixed templates (no ad-hoc additions).
- Per-obligation workers are stateless and single-turn.
- Validate file paths and line ranges in post-processing.
- Ensure 100% obligation coverage before Phase 2 starts.
- Phase 2A/2B outputs must use explicit file references with line ranges where possible.
- If `client_locations` are empty, require a justification in `client_code_gap` or `client_obligation_gap`.

## Open questions
- Canonical EIP file paths in the eips repo.
- Model selection + budget cap per obligation.
- Exact definition of obligation categories and enforcement types.
- Which client revision (submodule commit) should be treated as canonical for Phase 2?
