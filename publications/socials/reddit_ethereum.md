# r/ethereum Post

---

**Title:** We tested AI for EIP obligation verification — auditability improved faster than correctness, and that gap is the actual finding

**Subreddit:** r/ethereum

---

**Post body:**

I spent a month building [eip-verify](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40), an open-source tool that uses LLMs to extract obligations from EIPs and trace them through execution-specs and geth.

The tool runs in CI, produces inspectable artifacts at every phase, and we scored 47 obligation mappings across three Claude models on EIPs 1559, 2930, and 7702.

**The core finding:** the system got dramatically better at exposing where it might be wrong. It did not get dramatically better at being right. Auditability improved faster than correctness.

**What broke:**
- The same run produced a polished summary saying "all obligations verified" while the underlying data pointed to ABI wrappers and test files
- We had no rule for which output to trust when they contradicted each other
- 72% of follow-up burden (13/18 rows) came from the cheapest model tier alone

**What we built to fix it:**
An evidence governance pattern with five components — evidence hierarchy (raw artifacts beat narrative summaries), scoring rubric, contradiction register, claim ledger, and an iteration loop. Adapted from evidence-based medicine's approach to resolving conflicting sources.

**What this doesn't prove:**
- Autonomous verification readiness (not even close)
- Universal model rankings
- Cross-client generalization (geth-only so far)

Everything is open source. Tool, scored dataset, scoring rubric, contradiction register, evidence ledger — all linked from the repo.

Full write-up: [KILLER_PIECE_LINK]

Happy to answer questions about the architecture, the failure modes, or the evidence governance pattern.
