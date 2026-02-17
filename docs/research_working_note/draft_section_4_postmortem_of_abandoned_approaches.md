# IV. Postmortem of Abandoned Approaches

If this project had been written as a success narrative, this section would be short.

It should not be short.

The negative results are the most valuable part of the evidence because they show where reliability failed before the current design stabilized.

---

## 1) Why Include Failed Paths Explicitly

In security tooling, a rejection decision is only as credible as its evidence trail.

Saying "we tried X and it failed" is not enough. We need to know:
1. what X was supposed to improve,
2. what failure signal triggered abandonment,
3. what lessons were retained.

Current repository evidence supports this at a qualitative level, though not yet as a uniform benchmark protocol (`C011` in `docs/evaluations/evidence_ledger.md`).

---

## 2) Approach Class A: Repo-Map-Centric Discovery and Guided Flows

Relevant artifacts:
- `poc4/README.md`
- `poc4_5/README.md`
- `poc4_5/POC4_5_FLOW.md`

Observed pattern:
- Increasing context scope and layered guided prompts added operational complexity.
- Outputs were often rich in narrative detail but not consistently strong in location reliability.
- Reproducibility and diagnosis burden became difficult as workflow branches expanded.

This does not prove repo maps are universally ineffective. It shows that, in this context, added context breadth did not reliably translate into trustable per-obligation mappings.

Retained lesson:
- "More context" and "better verification" are not monotonic.

---

## 3) Approach Class B: Multi-Approach/Exploratory Spike Architectures

Relevant artifact:
- `poc/docs/SPIKE.md`

The spike program documented broad exploration (constants, guards, structural mapping, multi-step decomposition). This was useful for de-risking extraction patterns and proving incremental feasibility.

But it also exposed a governance problem:
- exploratory pipelines generated many intermediate outputs and variants,
- confidence semantics varied by phase,
- claim comparability across approaches remained weak without a single adjudication protocol.

Retained lesson:
- exploratory breadth is excellent for discovery;
- production trust requires narrowed evaluation contracts.

---

## 4) Approach Class C: Proposal-Era Rejection Matrix (Multi-agent, RAG, Symbolic Layers)

Relevant artifact:
- `poc5/docs/proposal/TECHNICAL_ARCHITECTURE_AND_DESIGN.md:66-72`

The proposal matrix labels several approaches as rejected or deprioritized (multi-agent systems, RAG pipelines, symbolic repo maps).

Evidence quality note:
- these conclusions are directionally consistent with the broader narrative,
- but they are not backed by a uniform, published, head-to-head benchmark in current artifacts.

Therefore, they should be treated as:
- **design postmortem evidence**,
- not definitive comparative science.

This distinction is essential to avoid the same overconfidence dynamic the essay critiques.

---

## 5) Why the Simpler Phase-Boundary Pattern Survived

Current implementation evidence suggests the surviving design won on operational traits:

1. predictable artifact lineage,
2. easier rerun semantics,
3. tighter dispute scope when a row looks wrong,
4. lower ambiguity in handoff between phases.

Relevant artifacts:
- `poc4_7/README.md:125-139`
- `poc5/docs/POC_IMPLEMENTATION_SPEC.md:58-69`
- `poc5/docs/POC_IMPLEMENTATION_SPEC.md:115`

This is a key thesis point:

> The selected pattern appears to have won on debuggability and auditability before it won on pure correctness.

That is not a weakness. In this domain, it is a practical prerequisite.

---

## 6) Postmortem Gaps Still Open

Even with the current design, three postmortem gaps remain:

1. No standardized stop criteria table for every abandoned approach.
2. No common metric frame to compare historical attempts directly.
3. No consolidated decision log linking each abandonment to explicit failure thresholds.

These are tracked in:
- `docs/evaluations/knowledge_gaps.md` (negative results documentation gap)
- `docs/evaluations/contradictions.csv` (especially CTR-008)

---

## 7) Practical Reading of This Section

What this section supports:
- why a simpler, artifact-first pipeline was selected.
- why complexity-heavy alternatives were operationally unattractive in this project state.

What this section does not support:
- universal rejection of multi-agent/RAG/symbolic methods in all code-verification settings.

---

## Transition to Section V

The postmortem narrows the design question.

Not: "Which architecture is theoretically strongest?"

But: **"What design pattern minimizes false confidence while preserving usable throughput?"**
