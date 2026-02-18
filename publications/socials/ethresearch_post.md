# LLM-Assisted EIP Obligation Verification: What 47 Adjudicated Mappings Reveal About Trust Calibration

## Summary

We built [eip-verify](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40), an open-source tool that uses LLMs to extract EIP obligations and trace them through execution-specs and client implementations (tested on geth). The pipeline runs in CI via GitHub Actions and produces structured, phase-by-phase verification artifacts.

After scoring 81 obligation mappings (47 directly adjudicated, 34 compare-derived proxy rows) across three Claude models (Haiku, Opus, Sonnet) on EIPs 1559, 2930, and 7702, the central finding is: **auditability improved faster than correctness across five PoC iterations.**

The system became dramatically better at exposing where it might be wrong. It did not become dramatically better at being right. This post presents the scored data, the evidence governance pattern we built in response, the failure modes we encountered, and open questions for the Ethereum research community.

---

## The Tool

`eip-verify` runs a five-phase pipeline:

```
extract → locate-spec → analyze-spec → locate-client → analyze-client
```

Each phase produces inspectable artifacts (CSV, JSON, prompts, model outputs). The final output is a per-obligation mapping with spec locations, client locations, and code flow analysis. Runs are triggered manually or via CI, and the full artifact chain is preserved for review.

- **Repo:** [github.com/petroslamb/eth-llm-poc](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40)
- **Example CI run:** [Run #21571909617](https://github.com/petroslamb/eth-llm-poc/actions/runs/21571909617)
- **Implementation spec:** [POC_IMPLEMENTATION_SPEC.md](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/POC_IMPLEMENTATION_SPEC.md)

---

## Scored Results

Obligation mappings were scored on five dimensions (statement fidelity, source location validity, implementation location validity, flow plausibility, evidence sufficiency) using a [fixed rubric](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/scoring_rubric.md). Each dimension: 0–2. Total: 0–10. Labels: `valid` (≥8), `partial` (5–7), `invalid` (≤4), `disputed` (contested requirement).

### Direct-adjudication block (47 rows, transcript/code-backed)

| Model | Rows | Avg (/10) | valid | partial | invalid | disputed |
|---|---:|---:|---:|---:|---:|---:|
| Haiku | 15 | 5.0 | 2 | 7 | 6 | 0 |
| Opus | 20 | 9.4 | 16 | 3 | 0 | 1 |
| Sonnet | 12 | 9.0 | 11 | 0 | 0 | 1 |

### Expanded block (81 rows, includes 34 compare-derived proxy rows)

| Model | Rows | Avg (/10) | valid | partial | invalid | disputed |
|---|---:|---:|---:|---:|---:|---:|
| Haiku | 49 | 3.5 | 2 | 7 | 39 | 1 |
| Opus | 20 | 9.4 | 16 | 3 | 0 | 1 |
| Sonnet | 12 | 9.0 | 11 | 0 | 0 | 1 |

Compare-derived rows use conservative proxy scoring from cross-run qualitative alignment — useful as triage signals, not a substitute for full adjudication.

### Follow-up Burden Concentration

**38.3%** of direct-adjudication rows (18/47) required manual follow-up (partial, invalid, or disputed). However, the burden is not uniformly distributed:

- **Haiku:** 13/18 follow-up rows (72.2%)
- **Opus:** 4/18 follow-up rows (22.2%)
- **Sonnet:** 1/18 follow-up rows (5.6%)

Excluding Haiku, follow-up burden drops to **15.6%** (5/32). This concentration was only discoverable because the evidence governance system tracked per-model, per-dimension breakdowns rather than aggregate pass/fail metrics.

---

## Evidence Governance: The Problem and the Pattern

### The Problem

During development, the same repository produced contradictory artifacts on a single run. A top-level summary claimed "all obligations properly mapped" while the underlying per-row data pointed to ABI wrappers, test files, and RPC helpers — none of which implement the logic the tool was verifying.

This was not a hallucination in the standard sense. The model generated both the data and the narrative from the same context. The narrative was more polished than the data. Without a rule for which source to prefer, the narrative would have won — because polished narratives always win when nobody is forced to check the underlying records.

We logged this as **CTR-001** in our [contradiction register](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv) and built a governance system to prevent similar failures from propagating silently.

### The Pattern

We assembled five interlocking components, adapted from evidence-based medicine's approach to handling conflicting sources. No single component is original — the integration is the contribution.

**1. Evidence Hierarchy.** Raw artifacts (CSVs, transcripts, prompts) beat validation documents (scored assessments), which beat narrative summaries. When tiers conflict, the lower tier wins. Three claims were downgraded via this rule.

**2. Multi-dimensional Scoring Rubric.** Five dimensions, 0–2 each. Total (0–10) maps to `valid`, `partial`, `invalid`, or `disputed`. Replaces subjective plausibility assessment with structured, repeatable judgment. [Rubric](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/scoring_rubric.md).

**3. Contradiction Register.** Disagreements between artifacts become tracked objects with IDs, conflicting claims, sources, and resolution rules. We surfaced 8 contradictions across 81 scored mappings. Before the register, all would have been resolved silently. [Register](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv).

**4. Claim Ledger.** Every external claim links to supporting evidence, a confidence level, and known counterevidence. Claims can only be promoted when evidence improves and must be downgraded when it weakens. No ledger entry means no external claim. [Ledger](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/evidence_ledger.md).

**5. Iteration Loop.** Run → Score → Log contradictions → Fix → Re-score → Repeat. Each cycle either promotes confidence or surfaces new contradictions. Both outcomes are productive.

---

## Five Things That Failed

**1. Evidence governance failed before generation failed.**
A polished narrative overrode contradictory row-level data because there was no source hierarchy. Without explicit contradiction tracking, teams default to whichever narrative sounds best.

**2. Model differences are error-profile differences, not accuracy ranks.**
Haiku's dominant failure mode is client-location noise (ABI wrappers, test files, engine-adjacent paths). Opus and Sonnet are stronger overall but still produce disputed obligations. Per-dimension error profiles are more actionable than global "model X is better" rankings.

**3. Obligation IDs are unstable across reruns.**
The same model on the same EIP produces different obligation IDs between runs. Row-by-row ID comparison is invalid as a regression method; statement-level semantic matching is required.

**4. Completeness metrics mask correctness failures.**
100% field population in output CSVs coexists with wrong spec/client location mappings. "All rows filled" is process telemetry, not quality evidence.

**5. Some obligations are semantically disputed.**
EIP1559-OBL-030 is the canonical case: the mapping mechanics look coherent, but the requirement itself may not be supported by the spec text. These need explicit `disputed` labels, not silent inclusion in compliance claims.

---

## Why Phase Boundaries Matter More Than Architecture

We tested several approaches before converging on the phase pipeline:

- Repo-map-heavy guided flows (high context breadth, low per-obligation trust)
- Exploratory multi-agent architectures (useful discovery, weak comparability)
- RAG-like layered retrieval (opaque error surfaces)

The surviving pipeline won on one criterion: **bounded adjudication cost with clear failure attribution.** Phase boundaries don't fix correctness, but they make errors inspectable and individually disputable. That turns iterative model improvement into auditable trust-calibration work.

---

## Limitations

- **No ground truth benchmark.** System-level precision/recall/F1 cannot be computed without benchmark-grade ground truth, which does not currently exist for EIP obligation verification.
- **Self-adjudicated scoring.** All 47 direct-adjudication rows were scored by the tool author. Inter-rater reliability is untested.
- **Single client.** Evidence is geth-only. Multi-client generalization is untested.
- **n=47 direct-adjudication.** Sample size limits statistical inference. This is evidence of pattern feasibility, not of statistical generalizability.

Defensible claim: *"This system accelerates obligation triage and evidence collection under explicit uncertainty controls."*

Not yet defensible: *"This system autonomously verifies protocol compliance with high confidence."*

---

## Open Questions

1. **Adjudication burden as KPI.** Is "reviewer minutes per obligation" a useful metric for protocol security tooling, or is there a better proxy for trust cost?

2. **Deterministic pre-filters.** We ran a [path-filter experiment](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/path_filter_experiment.md) where simple blocklist/allowlist rules flagged 67.6% of compare-block rows as noise-only. Has anyone else found deterministic guards effective as a triage layer before LLM-generated analysis?

3. **Disputed obligations.** How should tooling handle obligations where the requirement extraction itself is contested? We currently label them `disputed` and exclude from compliance claims.

4. **Multi-client generalization.** What are the practical blockers for extending this approach to besu, reth, or nethermind beyond changing the client repo path?

5. **External scoring.** Has anyone built multi-rater adjudication protocols for LLM-generated code analysis? Inter-rater reliability data would substantially strengthen (or weaken) the claims here.

---

## Resources

All evidence artifacts pinned to commit [`ca15d40`](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40):

- **Tool repo:** [github.com/petroslamb/eth-llm-poc](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40)
- **Scored dataset (81 rows):** [sample_scored_run.csv](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv)
- **Scoring rubric:** [scoring_rubric.md](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/scoring_rubric.md)
- **Evidence ledger:** [evidence_ledger.md](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/evidence_ledger.md)
- **Contradiction register:** [contradictions.csv](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv)
- **Qualitative evaluation:** [QUALITATIVE_EVALUATION.md](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/QUALITATIVE_EVALUATION.md)
- **Full research working note:** [research_working_note.md](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/research_working_note/research_working_note.md)
- **Metric derivations:** [metric_derivations.md](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/publications/evidence_governance_pattern/metric_derivations.md)
