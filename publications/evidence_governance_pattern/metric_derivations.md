# Metric Derivations for Evidence Governance Post

All figures derive from the 47 direct-adjudication rows in [`sample_scored_run.csv`](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv) and the per-model breakdown reported in the [Part 1 post](https://github.com/petroslamb/eth-llm-poc/blob/13260c8/publications/substack_post_v2.md).

## Per-Model Breakdown (47 direct-adjudication rows)

| Model | Rows | Avg Score (/10) | Valid (≥8) | Follow-up needed |
|---|---:|---:|---:|---:|
| Opus | 20 | 9.4 | 80% (16) | 20% (4 rows) |
| Sonnet | 12 | 9.0 | 92% (11) | 8% (1 row) |
| Haiku | 15 | 5.0 | 13% (2) | 87% (13 rows) |

Source: Part 1 post, "Per-model performance" table.

## Aggregate Burden

- Rows needing follow-up: 4 (Opus) + 1 (Sonnet) + 13 (Haiku) = **18**
- Total direct-adjudication rows: **47**
- Aggregate follow-up rate: 18 / 47 = **38.3%**

## Model-Tier Concentration

The aggregate 38.3% is heavily driven by Haiku, not evenly distributed:

- **Haiku contributes 13 of 18 follow-up rows = 72.2% of total burden**
- Non-Haiku (Opus + Sonnet) burden: 5 / 32 = **15.6%**
- Haiku burden: 13 / 15 = **86.7%**

### Effect Size (Haiku vs Non-Haiku)

| Metric | Value |
|---|---|
| Relative risk (follow-up) | 5.55× |
| Odds ratio | 35.1 |
| Fisher exact p-value | 4.75 × 10⁻⁶ |

The asymmetry is statistically unambiguous within this run family.

### Implication

The aggregate framing ("38.3% is the cost") can be read as "the method is expensive." The decomposition shows that governance exposed a model-tier asymmetry: most burden concentrates in triage-grade outputs, and model selection is itself an auditable governance decision.

## Other Cited Figures

### "8 contradictions surfaced across 81 scored mappings"

- 8: count of entries in [`contradictions.csv`](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv) (CTR-001 through CTR-008)
- 81: total rows in [`sample_scored_run.csv`](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv) (47 direct + 34 proxy)

## Caveat

These are PoC run-family statistics in one environment (Ethereum protocol verification with Claude models). Portability is plausible, not yet proven.
