# Phase Plan (Claude SDK, per-obligation mapping)

Goal: produce a complete, line-level mapping from the selected EIP obligations to the selected fork code. Each obligation must end with explicit evidence (function + line range) or an explicit gap classification. Target is 100% coverage.

## Phase 0A — Obligation extraction + indexing
Task:
- Read the selected EIP from the eips repo (or the provided path).
- Split compound obligations into atomic statements.
- If a requirement lists multiple constraints (e.g., upper/lower bounds, minimums), split them into separate obligations; do not drop any constraint.
- Parse obligations into a strict table with stable IDs.
- Tag each obligation with category and enforcement type (if applicable).

Output:
- Write a single CSV to a run folder under a timestamped directory.
- Path pattern: `notes/generated/<timestamp>/phase0A_runs/<timestamp>/obligations_index.csv`
- Columns (in order):
  - `id`
  - `category`
  - `enforcement_type` (empty if not applicable)
  - `statement` (atomic obligation)
  - `locations` (empty)
  - `code_flow` (empty)
  - `obligation_gap` (empty)
  - `code_gap` (empty)

## Phase 1A — Per-obligation implementation locations
Task:
- Read the CSV from Phase 0A.
- For each obligation row, locate all code paths that implement the obligation in the selected fork of execution specs.
- Ensure coverage of all viable paths, not just the most direct one.
- Include the enforcement point (predicate check or error) in the locations list.

Output:
- Update the same CSV (or write a new version alongside it) by filling the `locations` column.
- Locations format: a list of concrete references, e.g. `[path/file.py:L10-L42, path/other.py:function_name]`.

## Phase 1B — Code flow + gap analysis
Task:
- Read the CSV updated by Phase 1A.
- For each obligation row:
  - Map the complete end-to-end code flow and write it in `code_flow`, including the enforcement hop and at least one entry point.
  - Define and fill `enforcement_type` if not already set.
  - Identify gaps:
    - `obligation_gap`: missing or ambiguous spec requirement.
    - `code_gap`: missing or unclear implementation path.

Output:
- Update the same CSV (or write a new version alongside it) with filled `code_flow`, `enforcement_type` (if needed), and gap columns.

## Phase 2A — Client locations + code flow
Task:
- Read the CSV from Phase 1B.
- Create a new CSV that extends the Phase 1B columns with client-specific fields.
- For each obligation row, locate all relevant client code paths that implement the obligation:
  - Start with targeted search for EIP number (e.g., 1559) and specific keywords from `statement` and `code_flow`.
  - Use the initial matches to expand to surrounding code, dependencies, and related files as needed.
  - Record a best-effort set of locations (including enforcement points) and a concise client code flow with the enforcement hop and an entry point.

Output:
- Write a new CSV (do not overwrite Phase 1B output) under a timestamped run folder nested inside the Phase 1B run.
- Path pattern: `notes/generated/<timestamp>/phase0A_runs/<timestamp>/phase1A_runs/<timestamp>/phase1B_runs/<timestamp>/phase2A_runs/<timestamp>/client_obligations_index.csv`
- Columns (in order): all Phase 1B columns, plus:
  - `client_locations`
  - `client_code_flow`
  - `client_obligation_gap` (empty)
  - `client_code_gap` (empty)

## Phase 2B — Client gap analysis
Task:
- Read the CSV from Phase 2A.
- For each obligation row:
  - Review `client_locations` and `client_code_flow` to ensure coverage; expand searches if needed.
  - Identify gaps:
    - `client_obligation_gap`: client code paths that appear to implement behavior not covered by the obligation statement(s).
    - `client_code_gap`: missing or unclear client implementation for the obligation statement(s).
  - If new code is discovered, update `client_locations` and `client_code_flow` as part of the best-effort pass.
  - Remove any location that does not contain the key predicate/constant and record the gap.

Output:
- Write the updated CSV under a timestamped run folder nested inside the Phase 2A run.
- Path pattern: `notes/generated/<timestamp>/phase0A_runs/<timestamp>/phase1A_runs/<timestamp>/phase1B_runs/<timestamp>/phase2A_runs/<timestamp>/phase2B_runs/<timestamp>/client_obligations_index.csv`
- Columns remain the same as Phase 2A, with `client_obligation_gap` and `client_code_gap` filled.

## Execution notes
- Each phase writes to a timestamped run folder for repeatability and stores its prompts and outputs there.
- Each consecutive step nests its own timestamped run folder inside the previous step’s run folder, so later runs can vary while earlier steps remain fixed.
- Claude SDK workers may write to the CSV and can use all available filesystem tools.
