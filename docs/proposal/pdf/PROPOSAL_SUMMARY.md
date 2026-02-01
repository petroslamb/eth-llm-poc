# Proposal Summary (Submission Draft)

**Base repository URL (replace if needed):**
- https://github.com/petroslamb/eth-llm-poc/blob/main

This is a submission-ready proposal summary for the Ethereum Foundation RFP on LLM-assisted protocol security research. It is based on a working system (PoC 5) and includes a concrete, auditable path to production coverage across execution and consensus specifications and clients.

---

## Executive Summary
We propose a simple, auditable LLM-assisted verification system that ingests Ethereum specifications, maps EIP obligations to spec and client code, and produces reproducible discrepancy reports. The system already exists as PoC 5 for the execution layer, with CI integration and structured artifacts that support auditability. We intentionally avoided complex multi-agent architectures and RAG because they reduce reproducibility and increase failure modes; instead, we use direct chained phases with deterministic outputs and a proven production agent. The plan scales coverage across execution and consensus specs and their client implementations within 4–6 months, with optional phases that extend to broader protocol security mapping goals. The result is an immediately deployable workflow with clear phase boundaries, measurable outputs, and a realistic cost model.

---

## 1. RFP Objectives and How We Meet Them

| RFP Objective | How We Address It | Evidence |
| --- | --- | --- |
| Automated spec compliance | Extract obligations, map to spec + client code, produce gap reports | `poc5/docs/POC_IMPLEMENTATION_SPEC.md` |
| Workflow integration | Reusable GitHub Actions workflow with auditable artifacts | `poc5/docs/proposal/INTEGRATION_GUIDE.md` |
| Efficiency and accuracy | Deterministic phases, low false positives, optional LLM judge pass | `poc5/docs/proposal/EVALUATION_CRITERIA_RESPONSE.md` |

---

## 2. System Overview (Ingest → Analyze → Report)
**Ingest:** EIP markdown, execution-specs, and client repos.  
**Analyze:** chained phases (extract → locate spec → analyze spec → locate client → analyze client).  
**Report:** CSV indices, manifests, and summaries for auditability.

| Output | Purpose |
| --- | --- |
| `obligations_index.csv` | Spec-side obligation mapping |
| `client_obligations_index.csv` | Client-side mapping and gaps |
| `run_manifest.json` | Per-phase metadata for audit |
| `summary.md` / `summary.json` | Human + machine readable reports |

**Design principles:** simplicity, determinism, auditability, reproducibility.

---

## 3. Technical Approach (Methodologies, Frameworks, Tools)
**Methodology:** direct chained agent calls with strict phase boundaries and deterministic artifacts.  
**Rejected approaches:** loosely coupled multi-agent systems, MCP/A2A protocols, RAG, symbolic repo maps, and bleeding-edge research methods due to complexity and poor reproducibility.  
**Frameworks/models:** Claude Agent SDK with Opus 4.5 as primary, Sonnet 4.5 as fallback; evaluated GPT-5.2, Gemini 3 Pro, LangChain deep agent, and aider repomap.  
**Tools:** native filesystem and CLI tools with structured outputs and manifest metadata.

---

## 4. Deliverables and Acceptance Criteria

| Deliverable | Acceptance Criteria | Evidence |
| --- | --- | --- |
| Technical architecture & design | Architecture + approach cover ingest, analysis, report, and toolchain | `poc5/docs/proposal/TECHNICAL_ARCHITECTURE_AND_DESIGN.md` |
| Working prototype | PoC 5 runs per-EIP/per-client pipeline with artifacts | `poc5/docs/POC_IMPLEMENTATION_SPEC.md` |
| Integration guidelines | Reusable workflow integration documented | `poc5/docs/proposal/INTEGRATION_GUIDE.md` |
| Operations & extension | Setup, maintenance, and future phases documented | `poc5/docs/proposal/OPERATIONS_AND_EXTENSION.md` |

---

## 5. Project Plan and Timeline (4–6 Months)

| Phase | Timing | Outputs |
| --- | --- | --- |
| Phase 1 | Month 1 | Validate pipeline, harden phase separation, tighten prompts |
| Phase 2 | Month 2 | Execution clients matrix coverage, repeatable batch runs |
| Phase 3 | Month 3 | Consensus-specs ingestion and obligation extraction |
| Phase 4 | Month 4 | Consensus clients matrix, EL/CL linkage |
| Phase 5 (optional) | Month 5 | CI gating, quality thresholds, dashboarding |
| Phase 6 (optional) | Month 6 | Extended phases for broader protocol security mapping |

**Detailed plan:** `poc5/docs/proposal/PROJECT_PLAN_AND_TIMELINE.md`

---

## 6. Success Metrics (Planned Targets)
Targets are refined with EF during Phase 1, but tracked explicitly throughout:

| Metric | Target (Planned) | Evidence/Method |
| --- | --- | --- |
| Coverage | All selected EIPs per fork mapped to spec + client obligations | Pipeline artifacts and CSV indices |
| Accuracy | Low false positives, with optional LLM judge pass | Cross-model review and audit logs |
| Reproducibility | Deterministic artifacts for every run | Manifests + summary outputs |
| Throughput | Batch runs by EIP and client with reusable `eip-verify` unit | CI batch runs and job manifests |

---

## 7. Evaluation Criteria (RFP)

| Criterion | PoC Evidence | Future Expansion |
| --- | --- | --- |
| Scalability | Single EIP or batch; `eip-verify` unit scales across clients | Extend to consensus specs/clients and additional phases |
| Accuracy | Opus 4.5 yields minimal false positives; judge pass optional | Tune prompts, add evaluators, expand validation |
| Reliability | Simple chained pipeline with deterministic outputs | Add harnesses, logs, monitoring |
| Security | Runs inside CI; report-only outputs; minimal surface | Add tighter sandboxing as needed |

---

## 8. Budget and Cost Structure (EUR)
Costs include solo delivery estimates and LLM/CI usage for experimentation and batch runs.

| Cost Item | Estimate |
| --- | --- |
| Solo delivery (4 months, discounted) | EUR 53,760 |
| Solo delivery (6 months, discounted) | EUR 80,640 |
| LLM runs (Opus, 200/month) | EUR 6,751.20/month |
| LLM runs (Sonnet, 200/month) | EUR 4,050.72/month |
| CI (Linux baseline, 200 runs) | EUR 81.01/month |

**Full cost model:** `poc5/docs/proposal/BUDGET_AND_COST_STRUCTURE.md`  
**CSV breakdown:** `poc5/docs/proposal/BUDGET_AND_COST_STRUCTURE.csv`

---

## 9. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Spec ambiguity or EIP overlap | Explicit obligation extraction with audit trails |
| Model drift or regressions | Fixed prompts, versioned runs, optional judge pass |
| Cost variability | Clear run budgeting, batch scheduling, model fallback |
| Client divergence | Per-client runs, EL/CL separation, artifact comparisons |
| Over-complexity | Reject multi-agent and RAG to preserve determinism |

---

## 10. Vendor Background
Relevant background, tooling experience, and prior work are summarized in the vendor doc. References available on request.

**Docs:**  
`poc5/docs/proposal/VENDOR_BACKGROUND_AND_REFERENCES.md`  
`poc5/docs/proposal/resume2025_public.pdf`

---

## 11. Supporting Materials (Repository Links)
Append these to the base repository URL above:
- `/poc5/docs/proposal/TECHNICAL_ARCHITECTURE_AND_DESIGN.md`
- `/poc5/docs/proposal/PROJECT_PLAN_AND_TIMELINE.md`
- `/poc5/docs/proposal/BUDGET_AND_COST_STRUCTURE.md`
- `/poc5/docs/proposal/BUDGET_AND_COST_STRUCTURE.csv`
- `/poc5/docs/proposal/INTEGRATION_GUIDE.md`
- `/poc5/docs/proposal/OPERATIONS_AND_EXTENSION.md`
- `/poc5/docs/proposal/EVALUATION_CRITERIA_RESPONSE.md`
- `/poc5/docs/proposal/VENDOR_BACKGROUND_AND_REFERENCES.md`
- `/poc5/docs/proposal/PROPOSAL_READINESS_CHECKLIST.md`
- `/poc5/docs/proposal/Request for Proposal (RFP)_ Integrating Large Language Models (LLMs) into Ethereum Protocol Security Research.md`
