# Evaluation Criteria Response

This document summarizes how PoC 5 addresses the RFP evaluation criteria. Implementation details are in `poc5/docs/POC_IMPLEMENTATION_SPEC.md`.

## Summary Table

| Criterion | Response summary | Evidence |
| --- | --- | --- |
| Technical feasibility and innovation | Working multi-phase pipeline with spec indexing, client mapping, and reporting | `poc5/docs/POC_IMPLEMENTATION_SPEC.md` |
| Scalability and maintenance | Batch-capable workflows and reusable `eip-verify` units of work | `poc5/docs/proposal/INTEGRATION_GUIDE.md` |
| Accuracy | Model and methodology evaluation yielded low false positives on Opus 4.5 | `poc5/docs/proposal/TECHNICAL_ARCHITECTURE_AND_DESIGN.md` |
| Security and reliability | Deterministic artifacts, CI isolation, and minimal orchestration | `poc5/docs/POC_IMPLEMENTATION_SPEC.md` |
| Cost and timeline | Cost controls via configuration and a phased delivery plan | `poc5/docs/proposal/BUDGET_AND_COST_STRUCTURE.md`, `poc5/docs/proposal/PROJECT_PLAN_AND_TIMELINE.md` |
| Team expertise | Vendor background and case studies | `poc5/docs/proposal/VENDOR_BACKGROUND_AND_REFERENCES.md` |

## Scalability and Maintenance
- The PoC supports **single EIP runs** and **batch runs** for all EIPs in an execution fork.
- The **unit of work** is a reusable `eip-verify` job that scales in CI; this is demonstrated in the manual batch workflow.
- Future scalability extends the same unit of work to **consensus-specs** and **consensus clients**.
- Additional phases can scale coverage of protocol security mapping goals.

## Accuracy Strategy
- We evaluated a matrix of **methodologies, models, agents, and frameworks** and selected the current approach as the most accurate.
- Claude Opus 4.5 yields **low false positives**; remaining findings are low-impact and can be re-checked via an **LLM judge pass**.
- We manually validated accuracy using a second strong model (GPT-5.2 Codex High) to reduce single-model bias.
- Phases are **tunable and extensible**, enabling targeted improvements for extraction, mapping, and analysis.

## Reliability
- Reliability is driven by a **simple, chained pipeline** using a battle-tested agent with built-in tools.
- Each phase writes a `run_manifest.json` with inputs and environment metadata.
- Summaries prioritize the latest available CSV for consistent reporting.
- Artifacts are preserved per run for replay and inspection.
- Future work adds evaluation harnesses, logging, and monitoring for production-grade reliability.

## Security and Data Hygiene
- Runs execute in **GitHub Actions** with artifacts as outputs; the agent operates within a controlled CI environment.
- The pipeline produces reports rather than operational actions, reducing risk surface.
- API keys are injected via environment variables or secrets.
- Outputs are kept in run-local directories for isolation.
- Optional `.call.json` metadata supports auditability without exposing secrets.

## Cost Controls
- `--llm-mode fake` allows cost-free runs for CI and tests.
- `--max-turns` and phase selection limit model usage.
- See `poc5/docs/proposal/BUDGET_AND_COST_STRUCTURE.md` for budgeting guidance.
