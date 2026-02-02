# Budget and Cost Structure

This document describes the cost structure and budgeting model. Populate rate and quantity fields with vendor-specific inputs.

## Cost Categories

| Category | Basis | Typical drivers | Estimate |
| --- | --- | --- | --- |
| Engineering | Hours or sprints | Feature scope, integrations | See solo estimate below |
| LLM usage | Tokens or calls | Model, prompts, phase count | See LLM estimates below |
| Infrastructure | CI + storage | Artifact retention, run volume | See CI estimate below |
| Security review | Fixed or hourly | Data handling, auditability | TBD |
| Support/maintenance | Monthly retainer | Updates, triage, incident response | TBD |

## LLM Usage Model

| Variable | Meaning | Notes |
| --- | --- | --- |
| `tokens_in` | Input tokens per phase | Derived from prompt size |
| `tokens_out` | Output tokens per phase | Depends on model and max turns |
| `price_in` | Cost per 1M input tokens | Vendor pricing |
| `price_out` | Cost per 1M output tokens | Vendor pricing |
| `phases` | Phases per run | `extract`..`analyze-client` |
| `runs` | Runs per month | CI + manual |

**Estimated LLM cost per run (template):**
```
cost_per_run = phases * ((tokens_in / 1_000_000) * price_in
  + (tokens_out / 1_000_000) * price_out)
```

## LLM Cost Estimates (Assumptions Provided)

**Assumptions for experimentation:**
- Runs per month: **200**
- Tokens per run: **4M total**
- Split assumption: **3M input / 1M output** (75/25)
- Model pricing: use current vendor rates

### Pricing References (current, USD)
- Claude Opus 4.5: **$5/MTok input**, **$25/MTok output**
- Claude Sonnet 4.5: **$3/MTok input**, **$15/MTok output**
- Sonnet 4.5 has higher rates for prompts > 200K tokens
- Prompt caching can reduce repeated input costs

### FX Rate Used (USD -> EUR)
- **1 USD = 0.8439 EUR** (mid-market rate, 2026-02-01)

### Price Equivalents (approx, EUR)
- Opus 4.5: **EUR 4.22/MTok input**, **EUR 21.10/MTok output**
- Sonnet 4.5: **EUR 2.53/MTok input**, **EUR 12.66/MTok output**

### Experimentation Cost (200 runs/month)

**Opus 4.5 (converted to EUR)**
- Cost per run = `3*5 + 1*25 = $40` -> **EUR 33.76**
- Monthly cost = `200 * $40 = $8,000` -> **EUR 6,751.20**

**Sonnet 4.5 (converted to EUR)**
- Cost per run = `3*3 + 1*15 = $24` -> **EUR 20.25**
- Monthly cost = `200 * $24 = $4,800` -> **EUR 4,050.72**

### Batch Runs (EIPs × Clients)

Assumption: **clients = 10**. If the number of EIPs per batch is `E`, total runs = `E * 10`.

**Opus 4.5 (3M in / 1M out, converted to EUR):**
- Cost per run = **EUR 33.76**
- Batch cost = `E * 10 * EUR 33.76`

Examples:
- `E = 10` → 100 runs → **EUR 3,375.60**
- `E = 25` → 250 runs → **EUR 8,439.00**
- `E = 50` → 500 runs → **EUR 16,878.00**

**Sonnet 4.5 (3M in / 1M out, converted to EUR):**
- Cost per run = **EUR 20.25**
- Batch cost = `E * 10 * EUR 20.25`

Examples:
- `E = 10` → 100 runs → **EUR 2,025.36**
- `E = 25` → 250 runs → **EUR 5,063.40**
- `E = 50` → 500 runs → **EUR 10,126.80**

### Optional Cost Reductions
- **Prompt caching** reduces repeated input costs substantially.
- **Batch processing** can cut model costs for non-urgent runs.

## CI/Infrastructure Cost Model (Optional)

Estimate GitHub Actions usage with a per-minute rate and average run duration:

```
ci_cost = minutes_per_run * runs_per_month * rate_per_minute
```

Example: 60 minutes per run × 200 runs × **EUR 0.0067512/min**  
→ **EUR 81.01 per month** (Linux baseline).

## Engineering Cost Estimate (Solo Developer)

**Rate anchor (EU freelance benchmarks):**
- Average IT freelance rate: **EUR 104/hour**
- Consulting/management rate: **EUR 120/hour**

**Chosen list rate (senior solo delivery):**
- **EUR 120/hour** → **EUR 960/day** (8 hours)

**Discounted rate (30%):**
- **EUR 84/hour** → **EUR 672/day**

### Monthly and Project Totals (Solo)

Assuming **20 billable days/month**:
- **Monthly (list)**: 20 × EUR 960 = **EUR 19,200**
- **Monthly (discounted)**: 20 × EUR 672 = **EUR 13,440**

Project totals:
- **4 months (discounted)**: 80 × EUR 672 = **EUR 53,760**
- **6 months (discounted)**: 120 × EUR 672 = **EUR 80,640**

### Optional Range (if using average EUR 104/hour)
- **List**: EUR 832/day → **EUR 16,640/month**
- **Discounted (30%)**: EUR 582/day → **EUR 11,640/month**

## Payment Terms

| Cost Type | Payment Schedule | Notes |
| --- | --- | --- |
| LLM usage (Opus/Sonnet) | Upfront at project start | Covers monthly operational budget for runs |
| CI/Infrastructure | Upfront at project start | Covers GitHub Actions and storage |
| Engineering delivery | Monthly, or per milestone if delays occur | Invoiced at end of each month or upon milestone completion |

**Rationale:** Operational costs (LLM and CI) are consumed continuously throughout the project and require upfront allocation. Engineering effort is invoiced on a recurring basis, with flexibility to align with milestone delivery if project timelines shift.

## Cost Controls Available in eth-llm-poc
- `--llm-mode fake` for zero-cost CI and regression runs.
- `--max-turns` to limit conversation length.
- Phase selection to avoid unnecessary model calls.

## CSV Export
- Detailed numeric breakdowns live in [docs/proposal/BUDGET_AND_COST_STRUCTURE.csv](BUDGET_AND_COST_STRUCTURE.csv).
