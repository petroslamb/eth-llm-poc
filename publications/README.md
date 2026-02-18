# Publications Index

Evidence artifacts and publications from the eip-verify project.

---

## Articles

### Canonical Narrative (start here)

- **[Your AI Is Confidently Wrong — And You Have No Rule for What to Do About It](substack_post_killer.md)**
  Combined synthesis optimized for cross-platform distribution. Covers the trust gap, the five-component evidence governance pattern, and operational adoption steps.

### Deep Dives

- **[Measuring Trust: The Gap Between AI Auditing and Correctness](substack_post_v2.md)**
  Part 1 — full project narrative. Detailed setup, model comparison, phase architecture, CI deployment, and five things that broke.

- **[The Five-Component Pattern for AI Evidence Governance](evidence_governance_pattern/substack_post_evidence_governance.md)**
  Part 2 — pattern extraction with literature positioning. Evidence hierarchy, scoring rubric, contradiction register, claim ledger, and release gating.

### Other Formats

- **[ethresear.ch post](ethresearch_post.md)** — technical summary for Ethereum research audience

---

## Evidence Artifacts

All evidence artifacts pinned to commit [`ca15d40`](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40):

| Artifact | Description |
|---|---|
| [Scored dataset](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv) | 81 mappings, 47 direct-adjudication rows |
| [Scoring rubric](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/scoring_rubric.md) | Five-dimension quality assessment (0–10) |
| [Contradiction register](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv) | 8 tracked contradictions (CTR-001 through CTR-008) |
| [Evidence ledger](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/evidence_ledger.md) | Claim-level evidence tracking with counterevidence |

---

## Supporting Materials

- [Metric derivations](evidence_governance_pattern/metric_derivations.md) — burden concentration calculations (18/47, 13/18, 5/32)
- [Related work](evidence_governance_pattern/related_work.md) — literature positioning
- [Bibliography](evidence_governance_pattern/bibliography.md) — full reference list
- [Research findings](evidence_governance_pattern/research_findings.md) — detailed paper-by-paper analysis

---

## Distribution Assets

Social charts and visual assets for cross-platform promotion live in [`assets/`](assets/).
