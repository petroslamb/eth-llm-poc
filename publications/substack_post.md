# Our AI Verification Tool Got Better at Proving It Was Wrong — Not at Being Right

**What happens when you actually measure whether AI-generated security analysis is trustworthy**

---

One month ago, I set out to build an AI tool that could verify whether Ethereum clients actually implement what the protocol specification says they should.

The idea was straightforward: take an EIP (Ethereum Improvement Proposal), extract every obligation it imposes, then use an LLM to trace each obligation through the spec code and the client implementation. A verification pipeline. Automated. Systematic.

One month, five proof-of-concept iterations, and 47 directly adjudicated obligation mappings later, I can tell you something that surprised me:

**The system got dramatically better at exposing where it might be wrong. It did not get dramatically better at being right.**

To make that concrete: by the fifth iteration, the [evidence ledger](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/evidence_ledger.md) required every claim to link to an evidence artifact with a confidence tag, and provided structured fields for counterevidence. Earlier iterations had no comparable tracking process. The error *rate* didn't collapse, but the error *visibility* went from opaque to systematically auditable.

That gap — between auditability and correctness — turned out to be the most important finding of the entire project.

---

## The Setup

The tool, [eip-verify](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40), works in five phases. Given an EIP number, it:

1. Extracts every obligation from the EIP text
2. Locates where each obligation lives in the Python execution specs
3. Analyzes the spec code flow and flags gaps
4. Finds the corresponding implementation in the client (we tested with geth)
5. Analyzes the client code and maps it back to the obligation

Each phase produces inspectable artifacts — CSVs, JSON, the actual prompts and model outputs. You can trace any claim back to the exact moment the LLM made it. This turned out to matter more than I expected.

I ran it across three Claude models (Haiku, Opus, and Sonnet) on EIPs 1559 and 2930. The scored dataset has 47 directly adjudicated mappings — where I reviewed the model's transcript against actual source code — plus 34 compare-derived proxy rows from cross-run alignment scoring (primarily Haiku-family expansion).

I also ran EIP-7702 as a negative-control test. Run [`21570420032`](https://github.com/petroslamb/eth-llm-poc/actions/runs/21570420032) targeted geth `v1.13.14`, which predates 7702 support; the pipeline correctly reported the EIP as unimplemented. A [second run](https://github.com/petroslamb/eth-llm-poc/actions/runs/21571909617) completed cleanly with no false positives in that run. Both are excluded from the scored set.

Findings below draw from the 47 direct rows unless noted. Most come from EIP-1559; treat these as operational signal from a real codebase, not a benchmark-grade estimate.

---

## Five Things That Broke

### 1. The outputs contradicted each other — and both looked polished

Here's the moment that changed how I thought about this project. I now track it as [CTR-001](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv) in the contradiction register.

The run's summary narrative: *"All obligations properly mapped to specification and client implementation code."*

The same run's per-obligation data: client-location fields pointing to `accounts/abi/bind/bind.go` (an ABI wrapper), `ethclient/ethclient_test.go` (a test file), and `internal/ethapi/api.go` (an RPC helper) — none of which implement EIP-1559 transaction pricing logic.

Both documents were LLM-generated. Both were confident. The narrative said "verified." The data said "noisy." This is the core problem with LLM-generated analysis: **the failure mode isn't gibberish — it's plausible-sounding wrongness wrapped in confident language.** Without explicit rules for which evidence to trust when sources conflict, you default to whichever narrative sounds best.

### 2. Not all models fail the same way

Haiku was fast and cheap, but its client-location mappings were full of noise — test files, ABI wrappers, helper utilities that had nothing to do with the actual protocol logic. Opus and Sonnet were much stronger but still produced obligations where the requirement itself was debatable.

The useful insight isn't "Opus is better than Haiku." It's that **different models have different error signatures**, and you need to know your model's specific failure pattern, not just its benchmark score.

### 3. You can't compare runs by row ID

I assumed you could compare two runs by matching obligation IDs. You can't. The same model, same EIP, same config will produce different obligation IDs between runs. The numbering drifts. If you diff by ID, you get false disagreements everywhere.

This is a subtle trap: it *looks* like rigorous comparison, but the units don't correspond. Statement-level semantic matching is required instead.

### 4. "All fields filled" means nothing

One of the built-in summary metrics was field population: what percentage of columns are filled in the output CSV? Some runs hit 100%. That sounds great until you check what's in those fields and find wrong spec locations, irrelevant client paths, and hallucinated code flows.

**Completion is process telemetry. It is not quality evidence.** This distinction matters in any AI-assisted workflow, not just protocol verification.

### 5. Some requirements are genuinely contested

One obligation — OBL-030 for EIP-1559 — became my canonical example. The mapping mechanics looked perfectly coherent. The model found spec locations, client code, traced the flow. But the requirement itself might not actually be supported by the spec text. The *obligation extraction* was the problem, not the *obligation mapping*.

No amount of downstream accuracy fixes an upstream classification error. These need a `disputed` label, not silent inclusion in a compliance report.

---

## What Actually Improved

If correctness didn't improve dramatically, what did?

**Inspectability.**

Over five PoC iterations, I tried everything: multi-agent orchestration, repo-map-heavy guided flows, RAG-like layered retrieval. They all produced interesting results. None of them survived the operational test that mattered: *when the output is wrong, can you figure out where and why?*

The simple phase-boundary pipeline won because it produced a clear audit trail. Each phase has constrained outputs. You can replay any step. When something fails, you know which phase failed and what it was looking at. It's the difference between a debugging session and a mystery.

The scoring also improved. By the end, I had:
- A five-dimension rubric (statement fidelity, spec location validity, client location validity, flow plausibility, evidence sufficiency)
- A contradiction register tracking every conflict between artifacts
- A claim ledger with confidence tags on every finding
- An explicit separation between what the current data supports and what requires additional runs

None of this made the LLM smarter. All of it made the LLM's errors *findable*.

---

## The Number That Matters

Of the 47 obligation mappings I directly adjudicated (transcript/code-backed, not proxy scoring), **38.3% required manual follow-up** — partial, invalid, or disputed results that a reviewer would need to investigate.

That number is the real cost of this kind of system. Not the API bill. Not the token count. The reviewer hours.

For Opus, the follow-up rate is 20% (4 of 20 rows). For Sonnet, 8% (1 of 12). For Haiku, 87% (13 of 15). These aren't just model quality signals — they're *workload predictions*. If you're deploying this kind of tool, the cost-per-run metric that matters is cost-to-trust, not cost-to-generate.

---

## What You Can Defensibly Claim

If you're building LLM-assisted verification or analysis tools, there are two framings available to you:

**Defensible today:**
> This system accelerates obligation triage and evidence collection under explicit uncertainty controls.

**Not yet defensible:**
> This system autonomously verifies protocol compliance with high confidence.

The first is backed by the data. The second might become true eventually, but claiming it now, with current evidence, is a credibility risk. The gap between them is exactly the gap between auditability and correctness that this project surfaced.

---

## Three Predictions (Scoped to Early Operational Deployments)

1. Teams that measure adjudication burden (reviewer time per output) will deliver more stable quality than teams that optimize token spend alone.

2. Explicit `disputed` labeling will reduce expensive downstream reversals — because it forces disagreements to surface early rather than propagating through downstream reports.

3. Artifact-first reporting standards — where every claim links to inspectable evidence — will become a basic credibility filter for AI verification tooling.

These predictions are grounded in what we observed across two EIPs and three models. They may not generalize to all verification domains, but they're testable. If I'm wrong, the data trail exists to prove it.

---

## The Uncomfortable Meta-Observation

There's an irony I should name directly: much of the evidence governance infrastructure for this project — the rubrics, the contradiction register, the claim ledger — was itself built with AI assistance.

That's not a weakness. It's actually the most interesting thing about the project. The AI is mediocre at verifying protocol compliance. It's surprisingly good at building the scaffolding that exposes its own mediocrity. The question is whether the humans involved have the discipline to actually use that scaffolding instead of cherry-picking the results that sound best.

In my experience, that discipline is the hardest part. Harder than the engineering. Harder than the prompts.

---

## Where to Look

The tool is open source: **[eip-verify on GitHub](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40)**. The repo contains the [scored dataset](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/sample_scored_run.csv), [scoring rubric](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/scoring_rubric.md), [contradiction register](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv), and [evidence ledger](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/evidence_ledger.md).

If you're building something similar, the [twelve-step methodology](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/research_working_note/essay_methodology.md) for evidence-governed AI analysis may be more useful than the tool itself.

The strongest contribution of this project isn't a claim that verification is solved. It's a workflow that got better at exposing where it might be wrong.

In protocol security, that's the maturity signal that matters.

*Evidence links in this post are pinned to commit [`ca15d40`](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40).*
