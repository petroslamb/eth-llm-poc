# Technical Architecture and Design (Proposed System)

This document describes the **proposed system** based on the working PoC 5 implementation. It answers the RFP requirements for (a) how the system ingests specifications, analyzes code, and reports discrepancies, and (b) the technical approach, methodologies, frameworks, and tools.

## Scope and Intent
- **Baseline**: execution-specs + Geth client (PoC 5 today).
- **Expansion**: consensus-specs + consensus clients (planned).
- **Run model**: CLI + reusable CI workflows with deterministic artifacts.
- **Design principle**: keep the pipeline **simple, auditable, and repeatable**.

## System Overview (Ingest → Analyze → Report)

```
EIP Markdown + Specs + Client Repo
              |
       Spec/Code Indexing
              |
     Phase Pipeline (chained)
              |
   CSV + Manifests + Summaries
              |
     CI Artifacts + Reports
```

### Ingest Specifications
- **Execution-specs**: parse fork metadata and EIP lists from the repo, build a spec index, and validate EIP↔fork mappings.
- **Consensus-specs (planned)**: index fork docs and EIP listings, then align with fork activation metadata.
- **EIP text**: ingest the EIP markdown directly as the source of obligations.

### Analyze Code
The pipeline performs **direct chained agent calls** per phase:
1. **Extract** obligations from the EIP.
2. **Locate spec** implementations in specs (execution or consensus).
3. **Analyze spec** paths for missing or ambiguous behaviors.
4. **Locate client** implementations for each obligation.
5. **Analyze client** code for gaps and divergences.

### Report Discrepancies
- Generate **CSV indices** for obligation mappings and gap flags.
- Emit **phase manifests** for auditability.
- Produce **summary.md** and **summary.json** for human and machine consumption.
- Package outputs as CI artifacts for review and triage.

## Architecture (Based on PoC 5)

| Component | Responsibility | Evidence |
| --- | --- | --- |
| CLI entrypoint | Configuration, inputs, orchestration | `poc5/src/eip_verify/cli.py` |
| Pipeline | Phase sequencing and run layout | `poc5/src/eip_verify/pipeline.py` |
| Phase runner | Phase logic for extract/locate/analyze | `poc5/src/eip_verify/runner.py` |
| Spec indexer | Spec parsing + EIP↔fork mapping | `poc5/src/eip_verify/spec_index.py` |
| Reporting | Summary aggregation | `poc5/src/eip_verify/reporting.py` |
| CI workflows | Reusable workflow_call | `poc5/.github/workflows/ci.yml` |

## Technical Approach

### Methodologies
- **Chained, single-responsibility phases**: each phase produces a stable artifact for the next phase.
- **Deterministic regression runs**: fake mode generates repeatable outputs to validate prompts and reporting logic.
- **Audit-first outputs**: CSVs, manifests, and summaries enable manual review and reproducibility.

### Approaches Evaluated and Rejected
The following were prototyped and rejected due to complexity, unpredictability, or lack of productization:
- Loosely coupled multi-agent systems (harder reproducibility).
- MCP/A2A protocols (added coordination complexity).
- RAG pipelines (fragile retrieval, context drift).
- Symbolic repo maps/graphs (overhead, unpredictable results).
- Cutting-edge research approaches with limited production maturity.

### Chosen Approach (Simplest That Works)
- **Direct chained agent calls** with a strong production agent.
- **Filesystem-native tools** for repo analysis (read/write/grep/bash equivalents).
- **Minimal layers** between the LLM and the codebase to preserve traceability.

## Models, Frameworks, and Tooling

| Category | Decision | Rationale |
| --- | --- | --- |
| Primary agent | Claude Agent SDK | Best performance and reliability in PoC |
| Model | Claude Opus 4.5 (primary), Sonnet 4.5 (fallback) | Best accuracy in evaluations |
| Other models tested | GPT-5.2, Gemini 3 Pro | Lower overall performance for this task |
| Agent frameworks tested | LangChain Deep Agent, Aider + RepoMap | More complexity with weaker results |
| Future integration | LangChain (optional) | Only if required; base agent stays Claude |

## Evaluation Criteria Response (PoC + Proposed System)

### Scalability
- The PoC supports **single EIP runs** and **batch runs** for all EIPs in an execution fork.
- The **unit of work** is a reusable `eip-verify` job (scalable in CI); this is demonstrated in the manual batch workflow.
- Future scalability extends the same unit of work to **consensus-specs** and **consensus clients**, plus additional phases for protocol security mapping goals.

### Accuracy
- We evaluated a matrix of **methodologies, models, agents, and frameworks** and selected the current approach as the most accurate.
- Claude Opus 4.5 yields **low false positives**; remaining findings are typically low-impact and can be re-checked via **manual cross-model review** (used in the PoC). Automation of this step is optional future work.
- We manually validated accuracy using a second strong model (GPT-5.2 Codex High) to reduce bias from single-model evaluation.
- Phases are **tunable and extensible**, allowing targeted improvements to extraction, mapping, and analysis.

### Reliability
- Reliability is driven by a **simple, chained pipeline** using a battle-tested agent with built-in tools.
- The approach avoids extra orchestration layers that tend to introduce fragility.
- Future work adds **evaluation harnesses, logging, and monitoring** for production-grade reliability.

### Security
- Runs execute in **GitHub Actions** with artifacts as outputs; the agent operates within a controlled CI environment.
- The pipeline produces reports rather than executing operational actions, reducing risk surface.
- Additional security layers can be added around the agent runtime if required.

## Productionization and Reliability (Planned)
- **Prompt tuning and phase separation**: stricter boundaries, consistent inputs/outputs.
- **Logging and monitoring**: structured logs per phase, latency and cost tracking.
- **Evaluation harness**: regression suites using fake mode + curated gold runs.
- **Retry and partial run handling**: tolerate failures without losing artifacts.

## Client Coverage Strategy

Execution and consensus layers have **separate client matrices**, validated independently before cross-layer linkage. Client matrices are part of the proposed expansion.

| Layer | Clients (examples) | Coverage goal |
| --- | --- | --- |
| Execution | geth, besu, erigon, nethermind, reth | Per-client mapping and gap analysis |
| Consensus | lighthouse, prysm, teku, nimbus, lodestar | Per-client mapping and gap analysis |

## Optional Advanced Phases (Months 5–6)
- **CI gating outputs**: SARIF exports, policy thresholds, quality gates.
- **Cross-client divergence scoring**: rank inconsistent implementations.
- **Impact analysis**: surface RPC/config surfaces affected by spec changes.
- **Dashboards**: coverage progress and risk trends.

## Protocol Security Mapping Goals (Coverage Emphasis)
The design supports **future chained phases** that extend the pipeline to cover the goals below (and any additional, team‑agreed goals as scope evolves):
- Traceability from EIP obligations to spec and client code paths.
- Coverage gap detection across spec and client implementations.
- Divergence identification between spec formulas and client logic.
- Impact analysis of spec changes on code and interfaces.
- Attack-surface mapping for protocol-critical inputs.
- Prioritized review via structured outputs and ranking signals.
- Test adequacy linkage (planned) by tying obligations to test coverage.

## Summary
The architecture prioritizes **simplicity, determinism, and auditability**. The PoC 5 pipeline already demonstrates the core flow end-to-end. The proposed system extends it with stronger validation, separate client matrices for execution and consensus layers, and optional advanced phases to support CI gating and broader security mapping coverage.
