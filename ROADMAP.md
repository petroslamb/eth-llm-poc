# PoC 5 Roadmap (RFP-Aligned)

**Purpose:** Prioritized roadmap for the first draft RFP deliverable. This plan keeps the scope focused on execution-specs + geth for the proposal PoC, with consensus-specs deferred.

**Prioritization logic:** Items are ordered by what the RFP explicitly requires for a proposal-grade PoC (deliverables, objectives, and evaluation criteria), then by what improves credibility (accuracy, reliability, scalability), then by longer-term expansion.

## Priority 0 — Proposal-Critical PoC
These items are required for the proposal and must be present in the initial PoC delivery.

| Priority | Item | RFP Alignment |
| --- | --- | --- |
| P0 | End-to-end prototype on one client | Deliverable 2 (Prototype/PoC), Objectives 1–2 |
| P0 | Technical architecture & design doc | Deliverable 1 |
| P0 | Integration guidelines (CI-ready) | Deliverable 3, Objective 2 |
| P0 | Documentation for setup/maintenance | Deliverable 5 |
| P0 | Spec ingestion baseline (execution-specs) | Scope: Data ingestion, Objective 1 |
| P0 | EIP↔fork mapping from execution-specs | Objective 1, Evaluation: accuracy |
| P0 | Reporting & artifacts for auditability | Scope: Interface, Evaluation: reliability |

### P0.1 End-to-end prototype (execution-specs + geth)
- Demonstrate a full run that ingests execution-specs, maps EIP→fork, analyzes geth code, and outputs findings.
- Keep defaults aligned with current workflow: geth as default client, execution-specs mainnet branch, and a known EIP (e.g., 7702) mapped to its fork.
- Produce a reproducible run with artifacts (CSV + summary) suitable for proposal review.

### P0.2 Technical architecture & design doc
- Document the pipeline from spec ingestion → prompt generation → code analysis → reporting.
- Include data flow, components, inputs/outputs, storage layout, trust boundaries, and LLM-call lifecycle.
- Define how changes in specs are detected and how that influences re-runs.

### P0.3 Integration guidelines (GitHub CI)
- Provide a reusable workflow configuration that runs in external repos.
- Define required secrets, input options, and expected outputs.
- Add guidance for branch-based spec/client pinning and shallow checkouts.

### P0.4 Documentation for setup and extension
- Clear install/run instructions for the PoC package and workflow.
- Explain how to add a new EIP or change forks/clients.
- Document expected runtime, cost drivers, and artifact inspection.

### P0.5 Spec ingestion baseline (execution-specs)
- Ingest execution-specs on each run (shallow checkout) and index relevant spec files.
- Parse and structure spec sections used by the LLM prompts.
- Persist a spec snapshot per run to ensure reproducibility and traceability.

### P0.6 EIP↔fork mapping via execution-specs release table
- Use the execution-specs release table to map EIPs to forks programmatically.
- Validate that user inputs match the canonical mapping; flag mismatches in reports.
- Ensure the workflow surfaces a clear error when an EIP cannot be mapped.

### P0.7 Reporting & audit artifacts
- Emit structured reports (summary JSON/CSV + markdown summary).
- Upload all artifacts (inputs, prompts, outputs, intermediate files) from CI.
- Provide a “run manifest” to trace configuration, repo refs, and model settings.

## Priority 1 — Proposal-Strengthening Enhancements
These items increase technical credibility against evaluation criteria (accuracy, scalability, reliability).

### P1.1 Automated spec diffing & change detection
- Track changes between spec versions or branches to focus analyses on deltas.
- Allow “latest spec” runs with automated selection of the newest release.

### P1.2 Multi-client support (execution layer)
- Keep geth as default while enabling a client matrix for broader coverage.
- Aggregate findings across clients and report discrepancies.

### P1.3 Accuracy controls & validation
- Add static/semantic checks to reduce false positives.
- Include a triage tier for high-confidence mismatches vs. “needs review.”

### P1.4 Reliability & rate-limit resilience
- Add backoff/retry and circuit-breaker behavior for LLM calls.
- Capture partial-run summaries when failures occur.

### P1.5 Cost controls and model governance
- Add budget caps per run (max tokens or max turns per phase).
- Support model selection policies (cheap vs. thorough).

### P1.6 Security & data hygiene
- Redact secrets from logs and artifacts.
- Validate inputs to avoid unsafe shell interpolation or path injection.

## Priority 2 — Longer-Term Expansion
These items are out of scope for the initial proposal PoC but align with future milestones.

### P2.1 Consensus-specs ingestion and analysis
- Add consensus-specs parsing and fork mapping once execution pipeline stabilizes.
- Extend client analysis to consensus clients.

### P2.2 Cross-layer consistency checks
- Identify mismatches across execution and consensus rules.
- Flag spec inconsistencies that manifest as client divergence.

### P2.3 Scalable indexing & retrieval
- Build a persistent spec/code index for faster repeated runs.
- Add semantic search over specs and code for deeper comparisons.

### P2.4 QA benchmarks & evaluation metrics
- Construct a gold-standard test set of known EIP changes.
- Track precision/recall, runtime, and cost per EIP.

## Proposed sequencing for the proposal
1) Ship P0 items to meet RFP deliverables.
2) Add P1 items that directly address evaluation criteria (accuracy, reliability, scalability).
3) Schedule P2 items as Phase 2 of the grant/contract.
