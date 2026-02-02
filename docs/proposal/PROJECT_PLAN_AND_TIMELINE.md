# Project Plan and Timeline (4–6 Months)

This plan assumes PoC 5 is complete and outlines a 4–6 month roadmap. Dates are expressed relative to contract kickoff. The final two months are optional tracks that can be selected based on priorities.

## Assumptions

| Assumption | Value |
| --- | --- |
| Kickoff date | TBD (set at award) |
| Scope baseline | Execution-specs + Geth client, working pipeline |
| Expansion | Consensus-specs + consensus clients after baseline hardening |
| Run model | CLI + reusable GitHub Actions workflows |

## Planning Axes (tracked in parallel)

| Axis | Description | Outcome |
| --- | --- | --- |
| Pipeline hardening | Validation, phase separation, prompt tuning, deterministic regression runs | Stable, repeatable results |
| Execution layer coverage | Execution-specs + execution clients | Per-client verification runs and reporting |
| Consensus layer coverage | Consensus-specs + consensus clients | Per-client verification runs and reporting |
| Cross-layer linkage | Mapping EL/CL fork relationships | Combined analysis and traceability |

## Milestones (4–6 Months)

| Milestone | Timing | Dependencies | Key Deliverables |
| --- | --- | --- | --- |
| M0 (complete) | Done | — | Working CLI, reusable workflow, run artifacts |
| M1 | Month 1 | None | Ground truth dataset, accuracy baselines, prompt tuning |
| M2 | Month 2 | M1 accuracy ≥80% | Execution client matrix (3+ clients), batch coverage |
| M3 | Month 3 | Parallel to M2 | Consensus-specs ingestion, obligation extraction |
| M4 | Month 4 | M2 and M3 | Consensus client matrix, EL/CL linkage |
| M5 (optional) | Month 5 | — | CI gating, quality thresholds, dashboarding |
| M6 (optional) | Month 6 | — | Extended milestones, cross-client divergence scoring |

**Critical path:** M1 accuracy validation gates M2 expansion.  
**Contingency:** M5–6 absorb schedule slip from core milestones if needed.

## Client Coverage Expansion

Execution layer and consensus layer are treated as separate client matrices, each validated independently before cross-layer linkage.

| Layer | Clients (examples) | Coverage goal |
| --- | --- | --- |
| Execution | geth, besu, erigon, nethermind, reth | Per-client mapping and gap analysis |
| Consensus | lighthouse, prysm, teku, nimbus, lodestar | Per-client mapping and gap analysis |

## Pipeline Hardening Focus (Months 1–2)
- Validate current outputs against known EIP behaviors.
- Establish ground truth dataset for 2–3 well-understood EIPs.
- Improve phase separation (inputs/outputs, guardrails, and prompts per phase).
- Introduce regression suites for fake mode and deterministic snapshots.
- Define triage workflow for false positives/negatives and add review guidance.

## Optional Tracks (M5–M6)
- **CI gating outputs**: SARIF, policy thresholds, and automated quality gates.
- **Advanced analysis phases**: cross-client divergence scoring, impact prioritization.
- **Dashboards and reporting**: run history, client coverage status, risk trends.
- **Spec change monitoring**: automated spec diffs and re-validation triggers.
