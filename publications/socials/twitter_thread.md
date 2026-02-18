# Twitter/X Thread

Post as a thread (each `---` is a new tweet). Or collapse into a single tweet using just tweets 1 + 7.

---

**Tweet 1 (hook)**

Our AI verification tool produced a polished summary: "all obligations properly mapped."

The same run's data pointed to test files and ABI wrappers — none of which implement the logic it was supposed to verify.

Both were confident. Both were AI-generated. They contradicted each other.

🧵

---

**Tweet 2 (the gap)**

We had no rule for which output to trust.

No procedure for tracking the disagreement. No way to stop it from silently propagating into a compliance report.

This isn't a model problem. It's an evidence governance problem.

---

**Tweet 3 (the finding)**

After 47 adjudicated mappings across Ethereum EIPs and three Claude model tiers:

Auditability improved faster than correctness.

The system got dramatically better at exposing where it might be wrong. It did NOT get better at being right.

---

**Tweet 4 (the data surprise)**

72% of the follow-up burden (13/18 rows) came from the cheapest model tier alone.

We only found this because the evidence governance system made it visible.

Model choice isn't a cost decision. It's a governance decision.

---

**Tweet 5 (the medicine analogy)**

Medicine solved a version of this 30 years ago — evidence hierarchies that mechanically resolve conflicts between sources.

AI outputs need the same thing. Not better prompts. Not bigger models. A hierarchy.

---

**Tweet 6 (the pattern)**

We built a five-component pattern:

1. Evidence hierarchy (raw data > scored assessment > narrative)
2. Multi-dimensional scoring rubric
3. Contradiction register (disagreements are data)
4. Claim ledger (no claim without evidence + counterevidence)
5. Iteration loop

---

**Tweet 7 (CTA)**

The AI is mediocre at verification. It's surprisingly good at building the scaffolding that exposes its own mediocrity.

Generation is cheap. Trust is expensive. The expense isn't compute — it's honesty.

Full post + open-source tool: [KILLER_PIECE_LINK]

---

**Tweet 8 (optional — if driving to repo)**

Everything is open source:
• Contradiction register
• Claim ledger
• Scoring rubric
• Scored dataset (81 mappings)

github.com/petroslamb/eth-llm-poc
