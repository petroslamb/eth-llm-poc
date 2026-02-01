# PoC 5 Implementation Spec (eip-verify)

This document describes the **current, implemented** PoC 5 system in this repository. It is aligned to the RFP but intentionally scoped to **execution-specs + execution clients only** (consensus specs are deferred).

## 1) Purpose and scope

**Goal:** Provide a repeatable, CI-ready pipeline that extracts EIP obligations, maps them to execution-specs and a client implementation, and reports potential gaps. PoC 5 packages this as an installable CLI (`eip-verify`) and a reusable GitHub Actions workflow.

**In scope (current implementation):**
- Execution-specs indexing and EIP→fork mapping (from the execution-specs README).
- Multi-phase LLM pipeline (0A → 2B) against a **single execution client** per run.
- GitHub Actions workflows that shallow-clone dependencies and run the pipeline.
- Live LLM mode and a **fake mode** that records calls and generates deterministic outputs.

**Out of scope (current implementation):**
- Consensus-specs parsing.
- SARIF or code-scanning integration.
- Automated cross-client comparisons in a single run.
- Cost/cap caps or budget enforcement.

## 2) Package layout and entry points

PoC 5 is shipped as a Python package named `eip-verify`.

Key modules:
- `src/eip_verify/cli.py`: Fire-based CLI entrypoint (`eip-verify`).
- `src/eip_verify/runner.py`: Phase implementations (0A, 1A, 1B, 2A, 2B).
- `src/eip_verify/pipeline.py`: Orchestrates multi-phase runs.
- `src/eip_verify/spec_index.py`: Execution-specs indexing + EIP↔fork mapping.
- `src/eip_verify/reporting.py`: Aggregates run outputs into `summary.md` + `summary.json`.
- `src/eip_verify/fake_agent.py`: Fake LLM agent for offline/test runs.

## 3) Inputs and configuration

Primary inputs are provided via CLI flags (highest precedence), optional `config.yaml`, and environment variables.

**Required inputs for a full pipeline run:**
- `--spec-repo`: Path to **execution-specs** repository.
- `--client-repo`: Path to execution client (default target is **geth**).
- `--eip-file`: Path to EIP markdown file (from the EIPs repo).
- `--eip`: Numeric EIP id (e.g., `7702`).
- `--fork`: Execution-specs fork name (e.g., `prague`).

**Model control:**
- `--model`: Claude model name (e.g., `claude-sonnet-4-5`).
- `--max-turns`: Conversation turns per phase (default 20 in pipeline).
- `--allowed-tools`: Comma-separated tool list (defaults to `Read,Write,Bash,Grep,Glob`).

**LLM modes:**
- `--llm-mode live` (default for real runs): uses Claude agent SDK.
- `--llm-mode fake`: generates deterministic outputs + records call metadata.
- `--record-llm-calls`: writes `*.call.json` alongside each phase output.

**Environment variables:**
- `ANTHROPIC_API_KEY` (or `ANTHROPIC_AUTH_TOKEN`) required for `live` mode.
- `EIP_VERIFY_LLM_MODE` and `EIP_VERIFY_RECORD_LLM_CALLS` optional defaults.

## 4) Phase pipeline (implemented)

The pipeline executes phases in order and nests outputs. Phases are identified by user-facing names:

| Phase | CLI name | Purpose | Output CSV |
| --- | --- | --- | --- |
| 0A | `extract` | Extract obligations from EIP markdown; index specs | `obligations_index.csv` |
| 1A | `locate-spec` | Map obligations to execution-specs locations | `obligations_index.csv` (updated) |
| 1B | `analyze-spec` | Analyze spec code flow and spec-side gaps | `obligations_index.csv` (updated) |
| 2A | `locate-client` | Map obligations to client implementation locations | `client_obligations_index.csv` |
| 2B | `analyze-client` | Analyze client-side gaps | `client_obligations_index.csv` (updated) |

**Run structure (example):**
```
runs/<root>/
  phase0A_runs/<ts>/
    obligations_index.csv
    spec_index.json
    eip_fork_map.json
    spec_index_report.md
    phase0A_prompt.txt
    phase0A_output.txt
    phase0A_output.call.json   (if --record-llm-calls)
    run_manifest.json
    phase1A_runs/<ts>/...
      obligations_index.csv
      spec_map_check.json
      phase1A_prompt.txt
      phase1A_output.txt
      phase1A_output.call.json
      run_manifest.json
      phase1B_runs/<ts>/...
        obligations_index.csv
        phase1B_prompt.txt
        phase1B_output.txt
        phase1B_output.call.json
        run_manifest.json
        phase2A_runs/<ts>/...
          client_obligations_index.csv
          phase2A_prompt.txt
          phase2A_output.txt
          phase2A_output.call.json
          run_manifest.json
          phase2B_runs/<ts>/...
            client_obligations_index.csv
            phase2B_prompt.txt
            phase2B_output.txt
            phase2B_output.call.json
            run_manifest.json
  summary.md
  summary.json
```

**CSV outputs (where to look):**
- Phase 0A/1A/1B: `.../obligations_index.csv`
- Phase 2A/2B: `.../client_obligations_index.csv`

Each phase writes a **`run_manifest.json`** with run metadata (EIP, fork, client, config options, repo paths, and git info when available).

## 5) Spec indexing + EIP↔fork mapping

Phase 0A invokes `spec_index.write_spec_index_bundle`, which:
- Parses the **“Ethereum Protocol Releases”** table from execution-specs `README.md`.
- Extracts EIP lists per fork from the README and compares them to the fork’s `__init__.py` list.
- Writes:
  - `eip_fork_map.json` (fork list + mismatch data)
  - `spec_index.json` (spec repo path + git branch/commit + fork metadata)
  - `spec_index_report.md` (human-readable summary)
- Records any mismatches in the phase 0A `run_manifest.json` as `mismatch_forks`.

Phase 1A writes `spec_map_check.json` to confirm whether the selected fork’s README list agrees with the fork `__init__.py` EIP list.

## 6) Reporting (summary.md / summary.json)

After pipeline completion, `reporting.write_report` scans the run tree and produces:
- `summary.json`: structured metadata, phase list, latest manifests, and CSV analysis.
- `summary.md`: human-readable report including configuration, spec map status, and a table summarizing CSV population.

The summary chooses the **latest available CSV** in preference order: 2B → 2A → 1B → 1A → 0A. It also appends the **full CSV content** (up to size limits) to `summary.md`.

## 7) GitHub Actions workflows

PoC 5 includes reusable and manual workflows that **shallow-clone dependencies** and run the pipeline:

- `poc5/.github/workflows/ci.yml` (reusable `workflow_call`):
  - Inputs: EIP, fork, client, client ref, phases, model, max turns, EIPs ref, execution-specs ref, llm mode.
  - **No defaults** in this workflow; all inputs must be provided by the caller.
  - Shallow clones: `EIPs`, `execution-specs`, and a selected client (geth/besu/erigon/nethermind/reth).
  - Runs: `eip-verify pipeline ... --output-dir runs/ci_run`.
  - Uploads `runs/ci_run` as artifacts.

- `resolve_defaults.yml` (reusable `workflow_call`):
  - Central source of truth for defaults (including per-client refs).
  - Supports `profile=single|batch` to keep batch EIP defaults empty.
  - Manual workflows call this before invoking `ci.yml`.

- `manual_run.yml`: workflow_dispatch wrapper around the reusable workflow.
- `manual_run_batch.yml`: workflow_dispatch batch runner using `eip-verify get-matrix` to resolve EIPs for a fork.
- `test.yml`: unit/integration tests for the package.
- The manual workflow UI defaults are synced from `resolve_defaults.yml` via `scripts/sync_workflow_defaults.py`.

**Defaults (current, defined in `resolve_defaults.yml`):**
- **Single profile:** EIP `7702`, fork `prague`, client `geth`, phases `extract,locate-spec,analyze-spec,locate-client,analyze-client`.
- **Batch profile:** EIP defaults to **empty** (run all EIPs in fork), fork `prague`, client `geth`.
- Client refs: geth `v1.16.8`, besu `25.12.0`, erigon `v3.3.7`, nethermind `1.36.0`, reth `v1.10.2`.
- EIPs ref `master`, execution-specs ref `mainnet`, LLM mode `fake`, model `claude-opus-4-5`, max turns `20`, pypi package `.`.

## 8) Fake mode (deterministic test runs)

Fake mode replaces the live LLM calls and writes deterministic outputs:
- Writes a fake `obligations_index.csv` in Phase 0A.
- Populates client locations and gap fields in Phase 2A/2B.
- Writes `.call.json` records that include prompt, options, and metadata.

This allows CI and local testing without API calls while preserving the file layout and reporting behavior of a real run.

## 9) Known limitations and next steps

**Current limitations:**
- Consensus-specs are not indexed.
- No SARIF output or code-scanning annotations.
- No cost budgeting or per-phase throttling.
- The pipeline assumes EIP files are provided explicitly (or already available in the checkout).

**Planned improvements:**
- Add multi-client comparison runs and per-fork batches.
- Add SARIF export for CI gating.
- Expand spec parsing to consensus layer.

## 10) References

- Canonical RFP: `poc5/docs/proposal/Request for Proposal (RFP)_ Integrating Large Language Models (LLMs) into Ethereum Protocol Security Research.md`.
- Mapping goals: `poc5/docs/PROTOCOL_SECURITY_MAPPING_GOALS.md`.

## Appendix A) Operational runbook (copy/paste)

**Local run (live LLM):**
```sh
export ANTHROPIC_API_KEY="..."
eip-verify pipeline \
  --eip 7702 \
  --phases "extract,locate-spec,analyze-spec,locate-client,analyze-client" \
  --spec-repo ~/specs/execution-specs \
  --client-repo ~/clients/execution/geth \
  --eip-file ~/specs/EIPs/EIPS/eip-7702.md \
  --fork prague \
  --model claude-sonnet-4-5 \
  --max-turns 20 \
  --output-dir ./runs/manual_7702
```

**Local run (fake mode, no API calls):**
```sh
eip-verify pipeline \
  --eip 7702 \
  --phases "extract,locate-spec,analyze-spec,locate-client,analyze-client" \
  --spec-repo ~/specs/execution-specs \
  --client-repo ~/clients/execution/geth \
  --eip-file ~/specs/EIPs/EIPS/eip-7702.md \
  --fork prague \
  --llm-mode fake \
  --record-llm-calls \
  --output-dir ./runs/fake_7702
```

**Key outputs to verify:**
- `runs/<run_root>/summary.md` and `runs/<run_root>/summary.json`
- Latest CSV (preference order): `client_obligations_index.csv` (2B/2A) or `obligations_index.csv` (1B/1A/0A)
- Per-phase prompts/outputs: `phase*_*_prompt.txt`, `phase*_*_output.txt`, and optional `*.call.json`

**CI run (manual workflow_dispatch):**
```sh
# From the PoC 5 repo
gh workflow run "Manual Run" \
  -F eip=7702 \
  -F fork=prague \
  -F client=geth \
  -F client_ref=v1.16.8 \
  -F phases="extract,locate-spec,analyze-spec,locate-client,analyze-client" \
  -F model=claude-sonnet-4-5 \
  -F max_turns=20 \
  -F eips_ref=master \
  -F execution_specs_ref=mainnet \
  -F llm_mode=fake
```

**Download CI artifacts (from CLI):**
```sh
# Find the latest run for the workflow
gh run list --workflow "Manual Run" --limit 1

# Download artifacts for a specific run ID
gh run download <RUN_ID> --dir ./ci_artifacts
```

**CI run (reusable workflow_call from another repo):**
```yaml
name: Verify EIP

on:
  workflow_dispatch:

jobs:
  defaults:
    uses: petroslamb/eth-llm-poc/.github/workflows/resolve_defaults.yml@main
    with:
      profile: "single"

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
      max_turns: "20"
      eips_ref: "master"
      execution_specs_ref: "mainnet"
      llm_mode: "fake"
    secrets:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```
