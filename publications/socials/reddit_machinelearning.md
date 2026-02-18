# r/MachineLearning Post

---

**Title:** [P] Evidence governance for LLM outputs: a five-component pattern adapted from evidence-based medicine

**Subreddit:** r/MachineLearning

---

**Post body:**

I built an AI verification tool for Ethereum protocol security, scored 47 obligation mappings across three Claude model tiers, and found that **auditability improved faster than correctness** across five PoC iterations.

The most interesting result wasn't the model comparison — it was the evidence governance failure that happened first. The same run produced a polished summary claiming "all obligations verified" while the underlying per-row data pointed to irrelevant code locations. Both were LLM-generated, both were confident, and we had no rule for which to trust.

**The operational pattern we built:**

We adapted the Cochrane evidence hierarchy from evidence-based medicine to LLM outputs:

1. **Evidence hierarchy** — raw artifacts (CSVs, transcripts) beat validation docs, which beat narrative summaries. Mechanical tie-break when sources disagree.
2. **Multi-dimensional scoring rubric** — five dimensions (statement fidelity, source validity, implementation validity, flow plausibility, evidence sufficiency), 0–2 each, total 0–10.
3. **Contradiction register** — disagreements between artifacts tracked as first-class data with resolution rules. Surfaced 8 contradictions across 81 scored mappings; 3 claims downgraded.
4. **Claim ledger** — every external claim linked to evidence, confidence tag, and known counterevidence. No entry = no external claim.
5. **Iteration loop** — run → score → log contradictions → fix → re-score → repeat.

**Key quantitative finding:**

Overall follow-up burden was 38.3% (18/47 direct-adjudication rows), but 72.2% of that burden (13/18) concentrated in the cheapest model tier (Haiku). Without Haiku, burden drops to 15.6% (5/32). The governance system exposed model-tier asymmetry that would have been invisible in aggregate metrics.

**What this is NOT:**
- Not a benchmark (n=47, self-adjudicated, single domain)
- Not a model comparison paper (error profiles matter more than rankings)
- Not a claim that any of this is novel in isolation (the integration is the contribution)

**What might generalize:** The evidence hierarchy + contradiction register pattern should be applicable to any domain where LLMs produce both summaries and underlying evidence — compliance, code review, medical report generation, research synthesis. Tested in one environment only.

Open source: [github.com/petroslamb/eth-llm-poc](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40)

Full write-up: https://github.com/petroslamb/eth-llm-poc/blob/main/poc5/publications/substack_post_killer.md
