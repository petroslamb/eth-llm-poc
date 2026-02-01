# Project Plan and Timeline (4–6 Months)

This plan assumes PoC 5 is complete and outlines a 4–6 month roadmap. Dates are expressed relative to contract kickoff. The final two months are optional tracks that can be selected based on priorities.

## Assumptions

| Assumption | Value |
| --- | --- |
| Kickoff date | TBD (set at award) |
| Scope baseline | Execution-specs + Geth client, single-run pipeline |
| Expansion | Consensus-specs + consensus clients after baseline hardening |
| Run model | CLI + reusable GitHub Actions workflows |

## Planning Axes (tracked in parallel)

| Axis | Description | Outcome |
| --- | --- | --- |
| Pipeline hardening | Validation, phase separation, prompt tuning, deterministic regression runs | Stable, repeatable results |
| Execution layer coverage | Execution-specs + execution clients | Per-client verification runs and reporting |
| Consensus layer coverage | Consensus-specs + consensus clients | Per-client verification runs and reporting |
| Cross-layer linkage | Mapping EL/CL fork relationships | Combined analysis and traceability |

## Roadmap (4–6 Months)

| Phase | Timing | Focus | Key Deliverables |
| --- | --- | --- | --- |
| Phase 0 (complete) | Done | PoC 5 pipeline and workflows | Working CLI, reusable workflow, run artifacts |
| Phase 1 | Month 1 | Pipeline validation + phase separation | Regression baselines, prompt tuning plan, tighter phase boundaries, triage checklist |
| Phase 2 | Month 2 | Execution-specs client coverage | Client matrix plan, per-client runs, comparative reporting format |
| Phase 3 | Month 3 | Consensus-specs ingestion | Consensus spec indexer, fork/EIP mapping, consensus prompts |
| Phase 4 | Month 4 | Consensus client coverage + EL/CL linkage | Consensus client matrix, EL/CL fork linkage, joint reporting |
| Phase 5 (optional) | Month 5 | Advanced outputs and CI gating | SARIF export, policy thresholds, CI gating draft |
| Phase 6 (optional) | Month 6 | Research extensions | Additional analysis phases, cross-client divergence scoring, dashboards |

## Client Coverage Expansion

Execution layer and consensus layer are treated as separate client matrices, each validated independently before cross-layer linkage.

| Layer | Clients (examples) | Coverage goal |
| --- | --- | --- |
| Execution | geth, besu, erigon, nethermind, reth | Per-client mapping and gap analysis |
| Consensus | lighthouse, prysm, teku, nimbus, lodestar | Per-client mapping and gap analysis |

## Pipeline Hardening Focus (Months 1–2)
- Validate current PoC outputs against known EIP behaviors.\n- Improve phase separation (inputs/outputs, guardrails, and prompts per phase).\n- Introduce regression suites for fake mode and deterministic snapshots.\n- Define triage workflow for false positives/negatives and add review guidance.

## Optional Tracks (Months 5–6)
- **CI gating outputs**: SARIF, policy thresholds, and automated quality gates.\n- **Advanced analysis phases**: cross-client divergence scoring, impact prioritization.\n- **Dashboards and reporting**: run history, client coverage status, risk trends.\n- **Spec change monitoring**: automated spec diffs and re-validation triggers.
