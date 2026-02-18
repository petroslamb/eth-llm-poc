# The Evidence Governance Pattern We Built After Our AI Kept Confidently Lying to Us

**A five-component operational pattern for teams that need to trust LLM-generated analysis**

*This is for teams shipping LLM-assisted analysis in high-stakes workflows — protocol security, compliance auditing, code review — where "the model said so" isn't good enough.*

*Part 2 of [Our AI Verification Tool Got Better at Proving It Was Wrong — Not at Being Right](https://github.com/petroslamb/eth-llm-poc/blob/13260c8/publications/substack_post_v2.md)*

---

## The Problem

Last month, our AI verification tool produced a polished summary claiming "all obligations properly mapped" — while the same run's data pointed to ABI wrappers, test files, and RPC helpers that had nothing to do with the actual protocol logic. Both documents were confident. Both were AI-generated. They contradicted each other.

This isn't a bug in the model. It's a failure in evidence governance.

We had no rule for which artifact to trust when outputs disagreed. No procedure for tracking that disagreement. No way to prevent the contradiction from silently propagating into external claims.

Recent work makes this sharper: models hallucinate with high certainty even when they "know" the correct answer in nearby settings (Simhi et al., 2025). Confidence and correctness decouple in practice. And once report generation is cheap, the bottleneck shifts to tracing and verification effort (Rasheed et al., 2026). Our aim is not only higher answer quality; it is lower verification burden per claim, so auditing remains cheaper than redoing the analysis.

This post describes the operational pattern we built to fix that.

---

## What Exists and Where the Gap Is

Three streams of work address LLM trustworthiness, but none answers the operational question practitioners hit daily. Each stream solves part of the problem; the gap is in the space between them.

**Capability benchmarks** (HELM (Liang et al., 2023), hallucination studies) tell you how a model performs on standardized tasks. **Governance frameworks** (NIST AI RMF (Tabassi, 2023), safety-case work) tell you what organizational policies to have. **Claim-level verification** — the newest stream — is converging on tools for decomposing outputs into atomic claims, assigning per-claim verdicts, and surfacing disagreements as first-class signals (Rasheed et al., 2026; Ji et al., 2026; Chen, J. et al., 2025; Lu et al., 2025).

None of these answers: *when this specific run's summary contradicts its own underlying data, which artifact do you trust, and how do you make that decision repeatable across a team?*

Evidence-based medicine solved a version of this decades ago — the Cochrane hierarchy ranks RCTs above case reports above expert opinion (Sackett et al., 1996). We adapted that principle for LLM outputs. The result is a five-component pattern combining: evidence hierarchy, scoring rubric, contradiction register, claim ledger, and release gating. In our literature and repository scan, we did not find a widely adopted artifact-level pattern that integrates all five.

---

## The Five-Component Pattern

### 1. Evidence Hierarchy: Raw Artifacts Beat Narratives

Which evidence wins when sources disagree:

- **Tier 1 (strongest): raw run artifacts.** CSVs, model transcripts, prompts, phase outputs.
- **Tier 2: validation documents.** Row-level scoring with rubric-based adjudication.
- **Tier 3 (weakest): narrative summaries.** README prose, run summaries, retrospective commentary.

When tiers conflict, the strongest tier wins. This single rule prevents the most common failure mode: confident narrative overriding contradictory evidence. *Med-R²* (Lu et al., 2025) validates this independently — their system filters lower-level evidence when it conflicts with higher-level evidence, providing deterministic tie-break rules under conflict.

---

### 2. Scoring Rubric: Five Dimensions, Not Pass/Fail

Every mapping is [scored](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/scoring_rubric.md) on five dimensions (0–2 each):

1. **Statement fidelity** — does the obligation match the EIP text?
2. **Spec location validity** — does the cited spec code implement this?
3. **Client location validity** — is the cited client code relevant, or noise?
4. **Flow plausibility** — does the code-flow narrative connect entrypoint to enforcement?
5. **Evidence sufficiency** — enough artifact-level evidence to adjudicate?

Total (0–10) maps to: `valid` (≥8), `partial` (5–7), `invalid` (≤4), `disputed` (contested requirement). This replaces "looks plausible" with structured, repeatable judgment. *MedRAGChecker* (Ji et al., 2026) supports the design: multi-signal verification reduces false confidence compared with single-signal pass/fail.

---

### 3. Contradiction Register: Disagreements Are Data, Not Bugs

Contradictions between artifacts are [first-class workflow objects](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv). Each entry gets an ID, the conflicting claims with sources, a resolution rule, and a `tier_preferred` field that enforces the hierarchy mechanically.

**CTR-001 — the moment that changed how we work:** The run's narrative said *"all obligations properly mapped."* The same run's per-obligation CSV showed client-location fields pointing to `accounts/abi/bind/bind.go` (an ABI wrapper), `ethclient/ethclient_test.go` (a test file), and `internal/ethapi/api.go` (an RPC helper) — none of which implement EIP-1559 pricing logic. Before the register, the polished narrative would have silently overridden the noisy data. After, CTR-001 was logged, the narrative claim was downgraded, and the resolution rule was recorded for future runs.

Result: [8 contradictions](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv) surfaced across [81 scored mappings](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv), 3 claims downgraded. *Rethinking All Evidence* (Chen, J. et al., 2025) validates the approach — their system generates conflict flags with rationale and feeds them into synthesis instead of suppressing disagreement.

---

### 4. Claim Ledger: No Claim Without Evidence and Counterevidence

The [evidence ledger](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/evidence_ledger.md) ties every public-facing claim to supporting evidence, a confidence tag, and any known counterevidence. Claims can only be promoted when evidence improves, and must be downgraded when it weakens. No ledger entry means no external claim.

*From Fluent to Verifiable* (Rasheed et al., 2026) gives this a formal scaffold — their AAR framework defines provenance coverage, provenance soundness, contradiction transparency, and audit effort as measurable properties. Our ledger enforces the first three; the fourth (audit effort per claim) is our highest-priority unmade improvement.

*EviBound* (Chen, R., 2025) reinforces the enforcement side: claims only propagate with machine-checkable evidence. Their ablation data (hallucination rates: 100% → 25% → 0% as gates are added) provides directional evidence that dual gates outperform prompt-only setups.

---

### 5. The Operating Loop: How the Components Connect

The five components form an iterative loop:

**Run pipeline → Score obligations → Log contradictions → Apply fixes → Re-score → Repeat**

Each iteration either promotes claim confidence or flags new contradictions. Both outcomes are useful — the loop is productive even when things get worse, because deterioration is now visible and actionable.

*SOPBench* (Li et al., 2025) justifies this directly: across 24,000+ agent trajectories, many strong models sit in the 30–50% procedural compliance band. Outcome success does not guarantee procedural compliance. Our loop enforces that each cycle includes rubric scoring, contradiction logging, and ledger updating as mandatory steps.

Our target release discipline follows a dual-gate structure inspired by *EviBound*: **Gate A** validates the claim contract pre-execution; **Gate B** validates machine-checkable artifacts post-execution. We currently enforce these as manual checklist steps; full automation is planned but not yet implemented. Claims failing either gate are blocked from publication.

---

## What Changed When We Deployed It

**Before (CTR-001):** A polished narrative overrode contradictory row-level data. Nobody noticed because there was no rule for which source to prefer.

**After:** [8 contradictions](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv) surfaced across [81 scored mappings](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv). 3 claims downgraded. Error profiles characterized per model ([scored data](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv)): Haiku produces path noise (13/15 rows needed follow-up, avg 5.0/10 — derivation: [metric_derivations.md](https://github.com/petroslamb/eth-llm-poc/blob/main/publications/evidence_governance_pattern/metric_derivations.md)); Opus and Sonnet produce disputed obligations where the requirement itself is debatable.

[**38.3% of direct-adjudication rows**](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv) required manual follow-up. That number is the real cost — not the API bill, not the token count. The reviewer hours. The goal, as *From Fluent to Verifiable* frames it, is `E_verify ≪ E_generate` — verification effort much lower than generation effort. Our 38.3% sets the baseline; each governance iteration should reduce it.

The meta-irony: much of the governance scaffolding was itself built with AI assistance. The AI is mediocre at protocol verification. It's surprisingly good at building infrastructure that exposes its own mediocrity.

---

## How to Adopt This in Five Steps

You don't need the full stack on day one. Ordered by ROI:

1. **Create a contradiction register.** CSV is fine: ID, conflicting claims, sources, resolution rule, status. Forces the team to notice disagreements that currently get silently resolved.

2. **Start a claim ledger.** Every external claim gets an evidence link and confidence tag. Turns "we think X" into "we claim X based on Y, with known counterevidence Z."

3. **Define your evidence hierarchy.** Rank your artifact types. When they conflict, which wins? Even two tiers (raw output > summary) beats nothing.

4. **Build a scoring rubric.** What dimensions matter? Score them 0/1/2. Makes quality assessment repeatable.

5. **Gate external claims on the ledger.** No entry, no claim. Without this, everything above is optional documentation.

Start with 1 and 2. Formalize 3 and 4 as the team develops shared judgment. Step 5 is what makes the rest structural.

---

## What This Doesn't Solve

**Doesn't improve model accuracy.** The LLM is exactly as wrong as before. The pattern makes errors findable, not rare.

**Doesn't remove domain experts.** Someone still adjudicates. *SOPBench* shows even strong models fail required verification steps.

**Doesn't scale without reviewer time.** The governance *is* review time. The 38.3% rate is the cost of honest measurement.

**Doesn't survive gaming.** Garbage in the ledger, fake resolutions, rubber-stamped gates — the pattern is as strong as the team's commitment. As *The BIG Argument for AI Safety Cases* warns, safety cases become paperwork without the right operational mindset (Habli et al., 2025).

**Doesn't prove cross-domain transfer.** Tested in one environment: Ethereum protocol verification with Claude models. Likely portable, not proven portable.

The pattern makes trust decisions auditable, disputable, and updateable. It doesn't make them easy.

---

## Where to Look

The tool is open source: **[eip-verify on GitHub](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40)**. Governance artifacts:

- [Contradiction register](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv) (8 tracked contradictions)
- [Evidence ledger](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/evidence_ledger.md) (claim-level evidence tracking)
- [Scoring rubric](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/scoring_rubric.md) (five-dimension quality assessment)
- [Scored dataset](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv) (81 mappings, 47 direct-adjudication)

The strongest contribution isn't a claim that verification is solved. It's a workflow where every trust decision is inspectable, disputable, and updateable.

*Evidence links in this post are pinned to commit [`ca15d40`](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40).*

---

## References

- Chen, J. et al. (2025). *Rethinking All Evidence: Enhancing Trustworthy RAG via Conflict-Driven Summarization.* arXiv:2507.01281.
- Chen, R. (2025). *Evidence-Bound Autonomous Research (EviBound).* arXiv:2511.05524.
- Habli, I. et al. (2025). *The BIG Argument for AI Safety Cases.* arXiv:2503.11705.
- Ji, Y. et al. (2026). *MedRAGChecker: Claim-Level Verification for Biomedical RAG.* arXiv:2601.06519.
- Li, Z. et al. (2025). *SOPBench: Evaluating Language Agents at Following SOPs and Constraints.* arXiv:2503.08669.
- Liang, P. et al. (2023). *Holistic Evaluation of Language Models.* TMLR.
- Lu, K. et al. (2025). *Med-R²: Crafting Trustworthy LLM Physicians via EBM.* arXiv:2501.11885.
- Rasheed, R. A. et al. (2026). *From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents.* arXiv:2602.13855.
- Sackett, D. L. et al. (1996). *Evidence Based Medicine: What It Is and What It Isn't.* BMJ, 312(7023), 71–72.
- Simhi, A. et al. (2025). *Trust Me, I'm Wrong: LLMs Hallucinate with Certainty Despite Knowing the Answer.* arXiv:2502.12964.
- Tabassi, E. (2023). *AI Risk Management Framework (AI RMF 1.0).* NIST AI 100-1.
