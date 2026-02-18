# Metric Derivations for Evidence Governance Post

All figures derive from the 47 direct-adjudication rows in [`sample_scored_run.csv`](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv) and the per-model breakdown reported in the [Part 1 post](https://github.com/petroslamb/eth-llm-poc/blob/13260c8/publications/substack_post_v2.md).

## Per-Model Breakdown (47 direct-adjudication rows)

| Model | Rows | Avg Score (/10) | Valid (≥8) | Follow-up needed |
|---|---:|---:|---:|---:|
| Opus | 20 | 9.4 | 80% (16) | 20% (4 rows) |
| Sonnet | 12 | 9.0 | 92% (11) | 8% (1 row) |
| Haiku | 15 | 5.0 | 13% (2) | 87% (13 rows) |

Source: Part 1 post, "Per-model performance" table.

## Cited Figures

### "38.3% of direct-adjudication rows required manual follow-up"

- Rows needing follow-up: 4 (Opus) + 1 (Sonnet) + 13 (Haiku) = **18**
- Total direct-adjudication rows: **47**
- Rate: 18 / 47 = **38.3%**

### "Haiku produces path noise (13/15 rows needed follow-up, avg 5.0/10)"

- Haiku rows: **15**
- Follow-up needed: **13** (87%)
- Average score: **5.0 / 10**

### "8 contradictions surfaced across 81 scored mappings"

- 8: count of entries in [`contradictions.csv`](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv) (CTR-001 through CTR-008)
- 81: total rows in [`sample_scored_run.csv`](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv) (47 direct + 34 proxy)
