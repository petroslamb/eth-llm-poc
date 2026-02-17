# LLM-Assisted EIP Obligation Verification: What 81 Scored Mappings Reveal About Trust Calibration

## Summary

We built [eip-verify](https://github.com/petroslamb/eth-llm-poc), an open-source tool that uses LLMs to extract EIP obligations and trace them through execution-specs and client implementations (tested on geth). The pipeline runs in CI via GitHub Actions and produces structured, phase-by-phase verification artifacts.

After scoring 81 obligation mappings across three Claude models (Haiku, Opus, Sonnet) on EIPs 1559, 2930, and 7702, the main finding is not about model capability. It is about trust calibration: **auditability improved faster than correctness across our PoC iterations.**

This post summarizes what the scored data actually shows, what failed, and what we think matters for LLM-assisted protocol security tooling.

---

## The Tool

`eip-verify` runs a five-phase pipeline:

```
extract → locate-spec → analyze-spec → locate-client → analyze-client
```

Each phase produces inspectable artifacts (CSV, JSON, prompts, model outputs). The final output is a per-obligation mapping with spec locations, client locations, and code flow analysis. Runs are triggered manually or via CI, and the full artifact chain is preserved for review.

- **Tool repo:** [github.com/petroslamb/eth-llm-poc](https://github.com/petroslamb/eth-llm-poc)
- **Example CI run:** [Run #21571909617](https://github.com/petroslamb/eth-llm-poc/actions/runs/21571909617)
- **Implementation spec:** [POC_IMPLEMENTATION_SPEC.md](https://github.com/petroslamb/eth-llm-poc/blob/main/docs/POC_IMPLEMENTATION_SPEC.md)

---

## Scored Results

We scored obligation mappings on five dimensions (statement fidelity, spec location validity, client location validity, flow plausibility, evidence sufficiency) using a [fixed rubric](https://github.com/petroslamb/eth-llm-poc/blob/main/docs/evaluations/scoring_rubric.md). Labels: `valid` (≥8/10), `partial` (5-7), `invalid` (≤4), `disputed` (contested requirement).

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

Compare-derived rows are conservative proxy scoring from cross-run qualitative alignment — useful for triage signals, not a substitute for full adjudication.

**38.3%** of direct-adjudication rows required manual follow-up (partial/invalid/disputed).

---

## Five Things That Failed

**1. Evidence governance failed before generation failed.**
The same repo can produce polished but contradictory narratives. One run's README claims "full compliance" while spot-checks show noisy client mappings. Without source hierarchy and explicit contradiction tracking, teams default to whichever narrative sounds best. We now maintain a [contradiction register](https://github.com/petroslamb/eth-llm-poc/blob/main/docs/evaluations/contradictions.csv) as a required artifact.

**2. Model differences are error-profile differences, not accuracy ranks.**
Haiku produces high client-location noise (ABI wrappers, test files, engine-adjacent paths). Opus/Sonnet are materially stronger but still produce disputed obligations. Global "model X is better" claims are less useful than per-dimension error profiles.

**3. Obligation IDs are unstable across reruns.**
The same model on the same EIP produces different obligation IDs between runs. Row-by-row ID comparison is not a valid regression method. Statement-level semantic matching is required.

**4. Completeness metrics mask correctness failure.**
100% field population in output CSVs can coexist with wrong spec/client location mappings. "All rows filled" is process telemetry, not quality evidence.

**5. Some obligations are semantically disputed.**
EIP1559-OBL-030 is the canonical case: the mapping mechanics look coherent, but the requirement itself may not be supported by the spec text. These need explicit `disputed` labels, not silent inclusion in compliance claims.

---

## Why Phase Boundaries Matter More Than Architecture

We tried several approaches before converging on the phase pipeline:
- Repo-map-heavy guided flows (high context breadth, low per-obligation trust)
- Exploratory multi-agent architectures (useful discovery, weak comparability)
- RAG-like layered retrieval (opaque error surfaces)

The surviving pipeline won on one criterion: **bounded adjudication cost with clear failure attribution.** Phase boundaries don't fix correctness, but they make errors inspectable and disputable. That turns "model tuning" into auditable trust-improvement work.

---

## What This Does Not Prove

- System-wide precision/recall/F1 (no benchmark-grade ground truth yet)
- Universal model ranking across tasks and environments
- Autonomous low-risk verification readiness

We can defensibly claim: *"This system accelerates obligation triage and evidence collection under explicit uncertainty controls."*

We cannot yet claim: *"This system autonomously verifies protocol compliance with high confidence."*

---

## Open Questions for Discussion

1. **Adjudication burden as a KPI.** Is "reviewer minutes per obligation" a useful metric for protocol security tooling, or is there a better proxy for trust cost?

2. **Deterministic pre-filters.** We ran a [path-filter experiment](https://github.com/petroslamb/eth-llm-poc/blob/main/docs/evaluations/path_filter_experiment.md) where simple blocklist/allowlist rules flagged 67.6% of compare-block rows as noise-only. Has anyone else found deterministic guards effective as a triage layer before LLM-generated analysis?

3. **Disputed obligations.** How should tooling handle obligations where the requirement extraction itself is contested? We currently label them `disputed` and exclude from compliance claims, but there may be better approaches.

4. **Multi-client generalization.** Current evidence is geth-only. What are the practical blockers for extending this approach to besu, reth, or nethermind, beyond just changing the client repo path?

---

## Resources

- **Tool repo:** [github.com/petroslamb/eth-llm-poc](https://github.com/petroslamb/eth-llm-poc)
- **Scored dataset (81 rows):** [sample_scored_run.csv](https://github.com/petroslamb/eth-llm-poc/blob/main/docs/evaluations/sample_scored_run.csv)
- **Scoring rubric:** [scoring_rubric.md](https://github.com/petroslamb/eth-llm-poc/blob/main/docs/evaluations/scoring_rubric.md)
- **Evidence ledger:** [evidence_ledger.md](https://github.com/petroslamb/eth-llm-poc/blob/main/docs/evaluations/evidence_ledger.md)
- **Contradiction register:** [contradictions.csv](https://github.com/petroslamb/eth-llm-poc/blob/main/docs/evaluations/contradictions.csv)
- **Qualitative evaluation:** [QUALITATIVE_EVALUATION.md](https://github.com/petroslamb/eth-llm-poc/blob/main/docs/QUALITATIVE_EVALUATION.md)
- **Full research working note:** [research_working_note.md](https://github.com/petroslamb/eth-llm-poc/blob/main/docs/research_working_note/research_working_note.md)
