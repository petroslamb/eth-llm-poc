# Your AI Is Confidently Wrong — And You Have No Rule for What to Do About It

**Generation is cheap. Trust is expensive. The expense isn't compute — it's honesty.**

---

## The Moment Everything Changed

Our AI verification tool analyzed a complex codebase and produced two outputs from the same run.

The summary: *"All obligations properly mapped to specification and client implementation code."*

The underlying data: location fields pointing to an ABI wrapper, a test file, and an RPC helper — none of which implement the logic the tool was supposed to verify.

Both documents were AI-generated. Both were confident. They flatly contradicted each other.

And we had no rule for which one to trust.

No procedure for tracking the disagreement. No way to prevent it from silently propagating into a compliance report. The polished narrative would have won — because polished narratives always win when nobody is forced to check the receipts.

This wasn't a model failure. It was an *evidence governance* failure. And it's happening right now in any organization that ships AI-generated analysis without deciding, in advance, what counts as proof.

---

## The Finding That Changes What You Should Invest In

I spent a month building [eip-verify](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40), an AI tool for Ethereum protocol verification — checking whether client code correctly implements protocol specifications. Five iterations, 47 directly adjudicated obligation mappings, three Claude model tiers.

The core finding surprised me:

**The system got dramatically better at exposing where it might be wrong. It did not get dramatically better at being right.**

Over five iterations, I could trace every claim to the exact prompt, transcript, and code snippet that produced it. I could replay any phase independently. I could spot contradictions between the summary and the underlying data. The *inspectability* was genuinely excellent.

The *accuracy* was operationally useful at best. The strongest model scored 80% valid. The cheapest scored 13%. And 72% of the total follow-up burden came from the cheapest model alone (13 of 18 follow-up rows) — a fact we only discovered *because* the governance system made it visible.

Most teams building with AI are optimizing the wrong variable. They're trying to make the model right more often. What our data showed is that you should first make the model's *wrongness findable* — because findable wrongness is manageable, while confident wrongness is catastrophic.

This principle isn't specific to Ethereum or code verification. Any domain where an LLM produces both a summary and the evidence behind it — compliance auditing, code review, legal analysis, medical report generation, research synthesis — faces the same structural problem:

**The surface is always more polished than the substance. And without a rule for what to do when they disagree, the surface always wins.**

---

## Medicine Made This Mistake 30 Years Ago. We're Repeating It.

In the 1990s, medicine had its own version of this problem. Expert opinions sounded authoritative. Case reports were vivid. But when randomized controlled trials contradicted both — and they often did — nobody had a rule for which source to trust. Polished expertise overrode messy data, and patients paid for it.

The solution wasn't to train better experts. It was to build an **evidence hierarchy** — a mechanical rule that removes judgment from the conflict-resolution step. Systematic reviews over RCTs. RCTs over cohort studies. Cohort studies over case reports. No exceptions. No appeals to authority.

This reshaped how medicine evaluates evidence. And we're ignoring the lesson completely.

Right now, AI-generated analysis has the same structural problem medicine had before evidence-based practice: confident summaries routinely override their own underlying data, and organizations have no mechanical rule for resolving the conflict. Recent research confirms each piece independently — models hallucinate with certainty even when they know the answer (Simhi et al., 2025), multi-signal verification beats pass/fail (Ji et al., 2026), claim-level auditability is emerging as a field (Rasheed et al., 2026) — but in our literature and repository scan, we found no widely adopted pattern that integrates all the pieces into an operational workflow.

The practitioner's question remains unanswered: *when this specific run's summary contradicts its own data, which artifact wins?*

We built the answer.

---

## The Five-Component Pattern

We assembled five interlocking components, each simple on its own, powerful in combination. No single component is original — the integration is. Here's the full stack.

**1. Evidence Hierarchy.** Raw artifacts (CSVs, transcripts, prompts) beat validation documents (scored assessments), which beat narrative summaries. When tiers conflict, the strongest wins. Full stop. This single rule would have caught our opening contradiction — the CSV data (Tier 1) overrules the polished summary (Tier 3). Three claims in our project were downgraded this way.

**2. Multi-dimensional Scoring Rubric.** Every output is [scored](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/scoring_rubric.md) on five dimensions (0–2 each): statement fidelity, source location validity, implementation location validity, flow plausibility, and evidence sufficiency. Total (0–10) maps to `valid`, `partial`, `invalid`, or `disputed`. This replaces "looks plausible" with structured, repeatable judgment. Two reviewers scoring the same output should converge.

**3. Contradiction Register.** Disagreements between artifacts become [first-class workflow objects](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv) — tracked with an ID, conflicting claims, sources, and a resolution rule. We surfaced 8 contradictions across 81 scored mappings. Before the register, all would have been resolved silently — by whoever spoke last.

**4. Claim Ledger.** Every external claim links to supporting evidence, a confidence tag, and known counterevidence in the [claim ledger](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/evidence_ledger.md). Claims can only be promoted when evidence improves and must be downgraded when it weakens. No ledger entry means no external claim. This is the enforcement that makes everything else structural.

**5. Iteration Loop.** Run → Score → Log contradictions → Fix → Re-score → Repeat. Each cycle either promotes confidence or surfaces new contradictions. Both are productive. The loop works even when things get worse, because deterioration is now visible, not silently compounding.

---

## What Actually Happened When We Deployed This

**Before:** A polished AI narrative overrode contradictory row-level data. Nobody noticed because there was no rule for which source to prefer. Claims that should have been flagged shipped as stated.

**After:**

- 8 contradictions surfaced across 81 scored mappings — all previously invisible
- 3 claims downgraded based on tier-conflict resolution
- Model-tier asymmetry exposed: cheap models produced triage-grade output while only stronger models supported claim promotion
- Model choice became an auditable governance decision rather than a cost guess

The most surprising result was quantitative. The aggregate follow-up burden was 38.3% (18/47 direct-adjudication rows) — which sounds expensive until the governance system revealed that **72% of that burden was concentrated in the cheapest model tier** (13/18). Without it, follow-up drops to 15.6% (5/32). That single insight transformed an undifferentiated cost problem into an actionable routing decision: use stronger models where claims matter, cheaper models for bulk triage only.

The pattern didn't make the AI smarter. It made the AI's errors *findable*, and made the team *accountable* for what they chose to do with those errors.

---

## How to Start Tomorrow

You don't need the full pattern on day one. Ordered by ROI:

1. **Start a contradiction register.** A CSV is fine: ID, conflicting claims, sources, resolution rule. This single step forces the team to notice disagreements that currently get resolved by whoever speaks last. If you do nothing else, do this.

2. **Start a claim ledger.** Every external claim gets an evidence link and a confidence tag. Turns "we think X" into "we claim X based on Y, with known counterevidence Z."

3. **Define a two-tier evidence hierarchy.** Raw output beats summary. Even this minimal rule would have caught our opening contradiction.

4. **Build a scoring rubric.** What dimensions matter for your domain? Score them 0/1/2. Makes quality assessment repeatable across people and across time.

5. **Gate external claims on the ledger.** No entry, no publication. This makes the rest structural. Without it, everything above is optional documentation that will be abandoned under deadline pressure.

---

## What This Won't Fix

I want to be direct about the boundaries. The pattern doesn't make the AI smarter — errors become findable, not rare. Someone still adjudicates; domain experts aren't replaced. The governance *is* review time, and stronger models reduce it but don't eliminate it. It doesn't survive bad faith — garbage in the ledger means garbage out. And it's been tested in one environment: Ethereum protocol verification with Claude models. Portable in principle, unproven in practice.

---

## The Uncomfortable Truth

Here's the irony: much of the evidence governance infrastructure — the rubrics, the contradiction register, the claim ledger — was itself built with AI assistance.

The AI is mediocre at the verification task it was built for. It is surprisingly good at building the scaffolding that exposes its own mediocrity.

That's not a bug. That's the actual product.

The question was never "how accurate is the AI?" It was always "do the humans have the discipline to use the scaffolding instead of cherry-picking the results that sound best?"

In my experience, that discipline is the hardest part. Harder than the engineering. Harder than the prompts. Harder than choosing the right model.

Generation is cheap. Trust is expensive. And the expense isn't compute — it's the willingness to downgrade your own claims when the evidence says you should.

---

If you ship AI-generated analysis and don't yet have a contradiction register, start one this week. If you already track contradictions, gate your next external claim on the ledger. The pattern costs a CSV and an afternoon.

*The tool is open source: **[eip-verify on GitHub](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40)**. Evidence artifacts: [contradiction register](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv) · [claim ledger](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/evidence_ledger.md) · [scoring rubric](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/scoring_rubric.md) · [scored dataset](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv) (81 mappings, 47 direct-adjudication). Full evidence base: [Part 1 — the trust gap](https://github.com/petroslamb/eth-llm-poc/blob/13260c8/publications/substack_post_v2.md), [Part 2 — the governance pattern](https://github.com/petroslamb/eth-llm-poc/blob/13260c8/publications/evidence_governance_pattern/substack_post_evidence_governance.md). Evidence artifacts pinned to [`ca15d40`](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40); companion posts pinned to [`13260c8`](https://github.com/petroslamb/eth-llm-poc/tree/13260c8).*
