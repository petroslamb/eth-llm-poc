# Pipeline Brainstorming (PoC 5)

## Goals tied to the RFP
- Run the full spec→client comparison in CI (PRs or manual audit runs).
- Always capture reproducible evidence (spec/client SHAs, prompts, outputs, CSVs).
- Provide an inspectable report in GitHub Actions summaries.
- Keep a low-cost, repeatable test path for report rendering.

## Baseline workflow set (current + candidate)
- **Reusable pipeline (primary)**
  - `workflow_call` + `workflow_dispatch`.
  - Inputs: EIP, fork, client, model, phases, max_turns, refs.
  - Outputs: full run artifacts + summary.
- **Report-only fixture test (current)**
  - Validates report rendering without running LLM phases.
- **Report-only (generalized)**
  - Accepts a `run_root` or downloads a prior artifact, then renders a summary.
  - Lets reviewers reformat an existing run without rerunning the model.

## Optional extensions
- **Polling latest specs (SHA-change gating)**
  - Cron job pulls latest SHAs for execution-specs/EIPs/geth.
  - If unchanged, skip; if changed, run the pipeline.
  - Persist last-seen SHAs via cache or repo file.
- **Upstream-triggered runs**
  - `repository_dispatch` from specs/client repos when they change (requires cooperation).

## Reporting & summary ideas
- **HTML dropdowns** in `GITHUB_STEP_SUMMARY` for:
  - Each phase output (0A/1A/1B/2A/2B).
  - Last phase CSV as a rendered HTML table (for readability).
- **Report-only toggle**
  - Explicitly label fixture runs as test runs in job name and summary header.
- **Artifacts**
  - Always upload the full run directory so output matches local runs.

## Integration clarity
- Keep a single reusable workflow as the canonical pipeline.
- Keep a separate fixture test for reporting stability.
- Document call patterns for external repos (workflow_call).
