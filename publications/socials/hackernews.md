# Hacker News

---

## Submission (recommended: Show HN)

**Title:** Show HN: eip-verify – Evidence governance for AI-assisted Ethereum protocol verification

**URL:** https://github.com/petroslamb/eth-llm-poc/tree/ca15d40

*Alternative (if submitting the essay instead of the tool):*

**Title:** Auditability improved faster than correctness – lessons from AI-assisted EIP verification

**URL:** [KILLER_PIECE_SUBSTACK_URL]

---

## Author Comment (post immediately after submitting)

Author here. I built this recently as a proof of concept for the Ethereum Foundation's Protocol Security team.

The tool (eip-verify) uses Claude to extract obligations from Ethereum Improvement Proposals and trace them through specification and client code. It runs in CI and produces inspectable artifacts at each phase.

The main finding wasn't about model accuracy — it was that auditability improved much faster than correctness. The system got better at showing where it might be wrong without getting much better at being right.

The most useful thing we built was probably the evidence governance pattern: an evidence hierarchy (raw artifacts beat summaries), a contradiction register for when outputs disagree with each other, and a claim ledger that ties every external claim to evidence and counterevidence.

Key numbers (47 direct-adjudication rows): 72% of follow-up burden concentrated in the cheapest model tier (Haiku). Without Haiku, follow-up drops from 38.3% to 15.6%. Model choice turned out to be a governance decision, not just a cost decision.

The tool and all evidence artifacts are open source. Happy to answer questions about the architecture, the scoring rubric, or the failure modes we ran into.

Repo: https://github.com/petroslamb/eth-llm-poc/tree/ca15d40
