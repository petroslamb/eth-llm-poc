# PoC 5 Implementation Spec (RFP-aligned, built on PoC 4.7 package)

This spec uses the installable `poc4_7` package as the foundation and extends it to satisfy all RFP requirements. It is derived from the canonical RFP copy in `docs/Request for Proposal (RFP)_ Integrating Large Language Models (LLMs) into Ethereum Protocol Security Research.md` and the phase workflow in `poc4_7/PHASE_PLAN.md`.

## 1) Goals and success criteria

**Primary goal**: operationalize PoC 4.7 into a repeatable, CI-ready workflow that continuously checks client implementations against evolving Ethereum specifications and produces actionable mismatch reports.

**Success criteria (RFP-aligned):**
- **Spec parsing**: Extract obligations from execution specs and keep a versioned index tied to spec commits (consensus deferred).
- **Mismatch detection**: Produce structured, traceable findings per obligation with links to spec anchors and client code.
- **Workflow integration**: Support GitHub PR checks and scheduled (nightly/weekly) audits.
- **Accuracy**: Provide evidence-rich findings, confidence tagging, and “human review required” flags.
- **Scalability**: Run across multiple execution forks and EIPs (geth-only baseline) with bounded cost.
- **Documentation**: Provide setup, CI integration, maintenance, and extension guides.

## 2) Scope and non-goals

**In scope:**
- Execution specs only (consensus deferred to a later version).
- Execution client: **geth** as the default and only client for this PoC (other clients remain supported by `poc4_7` but are out of scope).
- Execution across multiple EIPs/forks, starting with one default set and expanding via config.
- Structured reporting outputs (JSON, Markdown, SARIF).
- CI integration (GitHub Actions).

**Out of scope for first draft:**
- Full automation of client checkout/updates beyond the workflow-controlled refs.
- Full ML evaluation harness (we will do lightweight validation and regression checks first).

## 3) Inputs and sources of truth

**Spec sources (workflow checkout):**
- `specs/execution-specs/`
- `specs/EIPs/`

**Client sources (workflow checkout):**
- `clients/execution/geth`

**Config inputs:**
- `poc4_7/config.yaml` extended to support EIP/fork mapping and geth-only defaults.

**Source-of-truth rules:**
- Spec branch (default `mainnet`) + commit hash + fork name are recorded in run metadata.
- EIP version and file path are recorded for each obligation.
- Client repo commit hash recorded per run.
- EIP-to-fork mapping is sourced from the execution-specs README “Ethereum Protocol Releases” table and recorded in run metadata.
- Fork `__init__.py` EIP lists are used as a verification source; mismatches are flagged in `eip_fork_map.json` and `run_manifest.json`.

## 4) Architecture overview

**Pipeline (base on PoC 4.7 phases):**
1. **Spec Indexing (new)**
   - Build a versioned `spec_index.json` and `obligations.json` keyed by obligation ID.
   - Parse the execution-specs README “Ethereum Protocol Releases” table into `eip_fork_map.json`.
   - Cross-check each fork’s `__init__.py` EIP list; flag differences for review.
   - (Optional) Record diff links between forks for faster follow-up analysis.
2. **Phase 0A (existing)**
   - Extract obligations from EIP/spec text into atomic statements.
3. **Phase 1A (existing)**
   - Map obligations to spec implementation locations.
4. **Phase 1B (existing)**
   - Describe spec code flow and spec-level gaps.
5. **Phase 2A (existing)**
   - Map obligations to client code locations and client code flow.
6. **Phase 2B (existing)**
   - Classify client gaps vs obligations.
7. **Reporting (new)**
   - Emit structured mismatch reports and summary artifacts.
8. **Batch Runner (new)**
   - Run client/EIP matrices and aggregate results.

## 5) Data model and artifacts

**Run metadata (new):**
- `run_manifest.json` (per run)
  - spec commit hash
  - fork
  - EIP id + file path
  - client repo + commit hash
  - model + prompt hashes

**Spec index (new):**
- `spec_index.json`
  - spec repo + commit
  - spec branch (default `mainnet`)
  - fork
  - list of EIP ids + doc anchors
 - `eip_fork_map.json`
  - fork name
  - EIP list (from execution-specs README “Ethereum Protocol Releases” table)
  - EIP list from fork `__init__.py` (verification)
  - mismatch flags and diffs (readme-only vs fork-only)

**Obligation index (existing):**
- `obligations_index.csv`
  - `id`, `category`, `enforcement_type`, `statement`, `locations`, `code_flow`, `obligation_gap`, `code_gap`

**Client obligations index (existing):**
- `client_obligations_index.csv`
  - all Phase 1B fields plus: `client_locations`, `client_code_flow`, `client_obligation_gap`, `client_code_gap`

**Mismatch reports (new):**
- `mismatches.json` (structured)
  - obligation id, spec anchor, client locations, mismatch type, severity, confidence, evidence
- `mismatches.md` (human-readable summary)
- `report.sarif` (GitHub code scanning compatible)

**Summary artifacts (new):**
- `summary.json` and `summary.md`
  - totals, coverage %, confidence distribution, unresolved gaps

## 6) CLI and package plan (PoC 4.7 as base)

**Keep:** `poc4_7` installable package (`pyproject.toml`, `poc4_7` CLI entrypoint).

**Add/extend:**
- `poc4_7 index-specs` to build `spec_index.json` + `obligations.json`.
- `poc4_7 index-specs` should also emit `eip_fork_map.json` with README + fork `__init__` verification.
- `poc4_7 report` to generate `mismatches.json`, `mismatches.md`, `report.sarif`.
- `poc4_7 batch` to iterate over client/EIP matrices.
- `poc4_7 ci` wrapper to integrate with GitHub Actions and emit SARIF/Markdown.

**Config extensions (proposed):**
- `spec_root`: execution-specs fork root (selected via EIP/fork map).
- `client`: default `geth` (others remain optional but out of scope here).
- `eip_fork_map_path`: path to parsed `eip_fork_map.json`.
- `report_formats`: `json,md,sarif`.
- `batch`: matrix settings (EIPs, forks; client fixed to geth).

## 7) CI/CD integration plan

**GitHub Action (new):**
- Inputs: EIP id, fork, spec root, model (client fixed to geth for this PoC).
- Outputs: SARIF + Markdown summary.
- Triggers: PR (narrow scope) + nightly (full matrix).

**CI behavior:**
- Manual (workflow_dispatch) runs support EIP/fork/client inputs for ad-hoc testing.
- Reusable (workflow_call) runs allow client repos (e.g., geth) to invoke the workflow directly.

## 8) Quality, reliability, and safety

**Determinism and reproducibility:**
- Fixed prompt templates and stable run folder structure.
- Run manifests with commit hashes.
- Cache intermediate results per obligation.

**Coverage:**
- Require 100% obligation coverage; missing coverage must be tagged as `unknown` with justification.

**Human review gating:**
- Low-confidence mismatches flagged as `review_required`.
- High-confidence mismatches become CI failures (configurable).

**Report-only validation (no LLM):**
- Maintain a fixture run under `poc4_8/tests/fixtures/` and use it for a CI job that runs `poc4_7 report` only.
- This validates the reporting mechanism without re-running the LLM pipeline.

## 9) Scalability and performance

**Batch processing:**
- Parallelize per obligation where safe.
- Limit concurrency by model budget.

**Incremental runs:**
- Skip unchanged obligations if spec hashes match.
- Reuse cached Phase 0A/1A outputs when only client changes.

## 10) Cost control

**Per-run cost controls:**
- Max tokens per obligation and per phase.
- Budget cap per batch run.

**Reporting:**
- Include cost estimate summary in `summary.json`.

## 11) Milestones and deliverables

**M1 — Package alignment + spec index**
- Implement `index-specs`.
- Add `run_manifest.json` and `spec_index.json`.
- Acceptance: spec index built for the latest execution fork and parsed `eip_fork_map.json` created from execution-specs README.

**M2 — Reporting formats**
- Implement `report` to emit JSON, Markdown, SARIF.
- Acceptance: `mismatches.json` + `report.sarif` generated for a sample run.

**M3 — Batch runner**
- Implement `batch` for EIP/fork matrices (geth-only baseline).
- Acceptance: multi-EIP run produces aggregated summaries for geth.

**M4 — CI integration**
- Provide GitHub Action + `ci` wrapper.
- Acceptance: PR run posts SARIF and summary.

**M5 — Execution-only stabilization**
- Harden execution-specs workflow and geth defaults (no consensus in this version).
- Acceptance: stable geth runs across at least two forks with reports.

**M6 — Documentation & handoff**
- Update `README.md` and `docs/` with workflow usage and integration steps.
- Acceptance: docs allow a new user to run locally and in CI.

## 12) Documentation plan

- `docs/IMPLEMENTATION_SPEC.md` (this document).
- `docs/PIPELINE_BRAINSTORMING.md` (workflow ideas and variants).
- `docs/PROTOCOL_SECURITY_MAPPING_GOALS.md` (RFP-aligned mapping goals).
- `docs/Request for Proposal (RFP)_ Integrating Large Language Models (LLMs) into Ethereum Protocol Security Research.md` (canonical RFP copy).
- Updates to `README.md` for usage and integration.

## 13) Risks and mitigations

- **Spec ambiguity**: mark `obligation_gap` and maintain traceable anchors.
- **LLM variance**: deterministic prompts + caching + regression checks.
- **False positives**: confidence thresholds + human review gating.
- **Cost blowups**: enforce per-phase budgets and concurrency caps.

## 14) Open questions / current decisions

- Baseline: use the latest execution-specs fork and EIP list available per the execution-specs README “Ethereum Protocol Releases” table at run time.
- Clients: execution-specs only; **geth** is the sole client for this PoC (consensus deferred).
- CI gating: default to fail only on **high-confidence** mismatches; review threshold later.
- Artifacts: keep fixture runs in-repo and upload full runs as CI artifacts.
