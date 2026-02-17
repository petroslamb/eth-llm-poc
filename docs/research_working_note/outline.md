# Detailed Outline: "The Trustworthiness Gap in LLM Protocol Verification"

**Subtitle:** Why Auditability Improved Faster Than Correctness in Ethereum EIP Mapping

**Target Length:** 4,500-5,500 words  
**Target Audience:** Protocol researchers, security engineers, AI tool builders  
**Tone:** Technical, skeptical, evidence-first

---

## Abstract (200 words)

**Core Thesis:**
- The central failure mode is not "LLMs cannot code"; it is "LLM outputs are easier to produce than to trust."
- Across PoC iterations, we improved traceability and reproducibility faster than we improved correctness.
- Phase-boundary pipelines did not solve correctness, but they made errors inspectable and disputable.
- The practical bottleneck became adjudication, not generation.

**One-sentence takeaway:**
If you cannot reliably falsify a mapping claim, you do not have a verification system; you have a persuasive report generator.

---

## I. Introduction: The Wrong Problem Statement (600 words)

### Opening Contradiction
- In one artifact set, outputs are presented as complete/compliant.
- In another artifact set for similar tasks, mappings are flagged as noisy or questionable.
- This contradiction is the essay entry point: confidence language outpaced evidence quality.

### Reframe
- Not a "capability gap" first.
- A **trustworthiness gap**: gap between produced claims and claims that can be independently validated.

### Definitions used in the essay
- **Traceability:** every claim points to inspectable evidence.
- **Falsifiability:** a reviewer can prove a claim wrong with bounded effort.
- **Reproducibility:** reruns preserve evidence structure and comparable outputs.

### Stakes
- In protocol security, false confidence is worse than explicit uncertainty.
- LLM-assisted workflows are useful only when uncertainty is surfaced, not hidden.

---

## II. System and Evidence Rules (700 words)

### What was built
- Multi-phase pipeline: extract -> locate-spec -> analyze-spec -> locate-client -> analyze-client.
- Structured artifacts: CSV, JSON, prompts, outputs, summaries.
- Scope: execution specs + execution client (geth for current evidence set).

### What evidence is admissible
- Tier 1: raw phase CSV + manifests + prompts/outputs.
- Tier 2: run summaries and qualitative evaluation docs.
- Tier 3: narrative readmes and retrospective notes.

### Why this hierarchy matters
- Many contradictions come from treating Tier 3 as equivalent to Tier 1.
- The essay uses strict source precedence and marks confidence per claim.

---

## III. What the Runs Actually Show (1,200 words)

### Finding A: Model behavior differs by error profile, not just "accuracy"
- Haiku: high noise in client mappings (frequent ABI/test/engine-adjacent drift in qualitative evaluation).
- Sonnet: stronger coverage and richer constraint language; can be verbose.
- Opus: strongest practical mapping quality in current evidence set; still misses or compresses constraints in some obligations.

### Finding B: Obligation identity is unstable across runs
- IDs are not stable; statement-similarity alignment is required.
- Implication: naive row-by-row diffing misleads reviewers.

### Finding C: "Complete CSV" is not "correct CSV"
- Population metrics (100% filled columns) are necessary but weak quality signals.
- High completion can coexist with wrong location selection.

### Finding D: Ambiguous obligations are structural risk
- Some obligations are extracted as hard requirements despite weak explicit support in spec text.
- These should be labeled "disputed" instead of silently merged into normal findings.

### Finding E: Clean runs can reflect environment alignment, not universal reliability
- EIP-7702 examples show both "missing feature" and "clean" outcomes depending on client ref/context.
- Good essay practice: interpret run outcomes with environment metadata, not in isolation.

---

## IV. Postmortem of Abandoned Approaches (900 words)

### Why this section is essential
- Negative results are the strongest credibility asset if documented cleanly.

### Approach classes and practical failure reasons
1. Multi-agent orchestration
- Too many moving parts, difficult blame assignment, low replay confidence.

2. Repo-map-heavy discovery
- Large context did not guarantee high-quality location retrieval.
- Added complexity without proportional reliability gains.

3. RAG-like layered retrieval plans
- Context drift and retrieval ambiguity created opaque error surfaces.

### Key insight
- The winning property was not theoretical elegance.
- It was **debuggability under disagreement**.

---

## V. The Trustworthiness Design Pattern (800 words)

### Pattern: Verification-first pipeline
1. Atomic phases with constrained outputs.
2. Artifact continuity between phases.
3. Mandatory evidence fields (locations + rationale).
4. Explicit uncertainty labels (`uncertain`, `ambiguous`, `disputed`).
5. Human adjudication gates on high-impact claims.

### Why phase boundaries helped
- They limited error propagation and made dispute scopes smaller.
- They transformed hidden failures into reviewable records.

### What they do not solve
- True semantic correctness.
- Obligation extraction subjectivity.
- Cross-run consistency by default.

---

## VI. Practical Framework for Builders (700 words)

### What to measure first
- Evidence quality metrics, not just output volume.
- Suggested baseline metrics:
  - location plausibility rate
  - disputed-obligation rate
  - adjudication time per obligation
  - rerun stability (statement similarity + location overlap)

### What to promise externally
- "Assisted triage with evidence trails," not autonomous verification.
- "Confidence-tagged hypotheses," not ground truth.

### Deployment playbook
1. Start single-client, narrow EIP scope.
2. Enforce source hierarchy and run metadata capture.
3. Add deterministic guards to block known noisy path classes.
4. Expand only after measured adjudication burden is acceptable.

---

## VII. Conclusion: From Capability Claims to Reliability Claims (500 words)

### Core conclusion
- The real progress in this project was methodological: we got better at proving ourselves wrong.

### Strong closing statement
- In security-critical code analysis, the primary product is not a mapping table.
- The primary product is a review process that survives disagreement.

### Falsifiable near-term predictions (conservative)
1. Teams that track adjudication workload will outpace teams that track only token/output metrics.
2. Verification pipelines with explicit uncertainty labels will produce fewer costly false positives in practice.
3. Tooling that optimizes auditability will be adopted faster than tooling that optimizes narrative fluency.

---

## Appendices

### Appendix A: Evidence Ledger Template
- claim
- artifact path
- evidence tier
- confidence
- counterevidence
- adjudication status

### Appendix B: Canonical Run Table
- run_id
- model
- EIP
- fork
- client ref
- known caveats

### Appendix C: Contradiction Register
- contradiction
- source A
- source B
- resolved/unresolved
- resolution note

### Appendix D: Reproducibility Checklist
- command lineage
- artifact completeness
- rerun comparability

---

## Draft Note to Author

Before full drafting:
1. Finalize evidence hierarchy and enforce it consistently.
2. Build a contradiction register; do not hide conflicting artifacts.
3. Remove unsupported architecture-ceiling claims unless quantified.
4. Use negative results as first-class evidence.
5. Keep every strong claim auditable to a concrete artifact path.
