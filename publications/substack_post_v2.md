# Measuring Trust: The Gap Between AI Auditing and Correctness

**Auditability improved faster than correctness — and that changes what you should invest in**

---

## The Problem Nobody Wants to Hear About

Every blockchain runs on a promise: the code does what the spec says it should.

For Ethereum, that promise passes through a chain of documents and codebases. An EIP (Ethereum Improvement Proposal) describes a protocol change in human language — think "this is how the new fee calculation must work." That proposal gets translated into a formal Python reference called the [execution specs](https://github.com/ethereum/execution-specs). Then independent teams — geth in Go, Reth in Rust, Besu in Java — write their own implementations from the same spec. If any client gets it wrong, the network can fork.

The Ethereum Foundation's Protocol Security team audits this chain manually. They read the EIP, read the spec code, read the client code, and check that the obligations line up. It's slow, expert-level work, and it has to happen every time the protocol changes. The Foundation [issued an RFP](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/proposal/Request%20for%20Proposal%20%28RFP%29_%20Integrating%20Large%20Language%20Models%20%28LLMs%29%20into%20Ethereum%20Protocol%20Security%20Research.md) asking whether LLMs could help.

I built a proof of concept to find out. Five iterations, one month, 47 directly adjudicated obligation mappings later, I can tell you something that surprised me:

**The system got dramatically better at exposing where it might be wrong. It did not get dramatically better at being right.**

That gap — between auditability and correctness — turned out to be the most important finding of the entire project. And it applies far beyond Ethereum.

---

## The Setup

The tool, [eip-verify](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40), works in five phases. Given an EIP number, it:

1. Extracts every obligation from the EIP text
2. Locates where each obligation lives in the Python execution specs
3. Analyzes the spec code flow and flags gaps
4. Finds the corresponding implementation in the client (we tested with geth)
5. Analyzes the client code and maps it back to the obligation

Each phase produces inspectable artifacts — CSVs, JSON, the actual prompts and model outputs. You can trace any claim back to the exact moment the LLM made it. This turned out to matter more than I expected.

### Why These EIPs

Not all EIPs are equally useful for testing a verification tool. I chose three deliberately:

- **EIP-1559** — the fee-market overhaul. Complex, mature, deeply embedded in client code. Most of the scored data comes from here. This is the stress test.
- **EIP-2930** — access list transactions. Structurally simpler. Good for establishing a baseline and confirming the pipeline works on a less complex obligation set.
- **EIP-7702** — a recent Prague-fork addition. Used as a **negative control**: run [`21570420032`](https://github.com/petroslamb/eth-llm-poc/actions/runs/21570420032) targeted geth `v1.13.14`, which predates 7702 support, and the pipeline correctly reported the EIP as unimplemented. A [second run](https://github.com/petroslamb/eth-llm-poc/actions/runs/21571909617) completed cleanly against a supporting version. Both are excluded from the scored set.

The scored dataset has 47 directly adjudicated mappings — where I reviewed the model's transcript against actual source code — plus 34 compare-derived proxy rows from cross-run alignment scoring (primarily Haiku-family expansion).

Findings below draw from the 47 direct rows unless noted. Most come from EIP-1559; treat these as operational signal from a real codebase, not a benchmark-grade estimate.

---

## The Agent: Deliberately Simple

A common assumption in AI tooling is that more sophisticated orchestration produces better results. Five iterations of this project taught me the opposite.

The "agent" in eip-verify is an LLM with file-system access — read, write, bash, grep, glob — and a capped number of conversation turns. That's it. No multi-agent framework. No retrieval-augmented generation. No custom orchestration. The total agent adapter is [~80 lines of Python](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/src/eip_verify/agents.py).

I used Claude (via the Claude Agent SDK) because the SDK made this workflow trivial: give the model shell access, point it at a codebase, constrain its turns, capture everything it produces. The same architecture should be portable to other tool-using LLMs — OpenAI's function calling, local models with tool support — though we haven't tested that claim.

Earlier iterations tried harder:
- **Repo-map-heavy guided flows** (PoC 4.x): High context breadth increased complexity and diagnosis cost without reliable trust gains.
- **Exploratory multi-agent architectures** (PoC 1): Useful discovery power, weak comparability unless constrained by a single adjudication contract.
- **RAG-like layered retrieval**: Opaque error surfaces — when something went wrong, you couldn't tell where.

The simple pipeline won because of one criterion: **when the output is wrong, can you figure out where and why?**

### Why Phase Boundaries Are the Key Design Choice

Phase boundaries aren't just an organizational convenience. They solve four specific problems that every LLM-on-codebase system hits:

1. **Fresh context per phase.** Each phase starts with a clean context window. The model receives only the previous phase's structured CSV output — not the accumulated context, reasoning traces, and dead ends from all prior phases. This prevents error compounding: a bad location guess in phase 1A doesn't silently bias the code-flow analysis in phase 1B.

2. **Constrained input/output contracts.** Each phase has a defined input (the EIP text, or the previous CSV) and a defined output (an updated CSV with specific columns filled). When a phase produces garbage, you know exactly which contract it violated and what it was looking at when it failed.

3. **Single-phase replay.** You can re-run any individual phase without re-running the entire pipeline. If locate-client produces noisy mappings, you can adjust the prompt or model for that phase alone, re-run it, and compare results — without touching the obligation extraction or spec analysis that already looked correct.

4. **Decomposed focus.** Instead of asking the model to "verify this EIP end-to-end" (a task that requires holding the EIP text, the spec code, and the client code in working memory simultaneously), each phase gives the model one tractable job. "Extract the obligations." "Find where this obligation lives in the spec." Each phase gets a fresh look at a focused question, which is where LLMs perform best.

Complex orchestration makes errors systemic and invisible. Phase boundaries make them localizable and disputable. For security-critical work, that tradeoff isn't close.

---

## Five Things That Broke

### 1. The outputs contradicted each other — and both looked polished

This is the moment that changed how I thought about this project. I now track it as [CTR-001](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv) in the contradiction register.

The run's summary narrative: *"All obligations properly mapped to specification and client implementation code."*

The same run's per-obligation data: client-location fields pointing to `accounts/abi/bind/bind.go` (an ABI wrapper), `ethclient/ethclient_test.go` (a test file), and `internal/ethapi/api.go` (an RPC helper) — none of which implement EIP-1559 transaction pricing logic.

Both documents were LLM-generated. Both were confident. The narrative said "verified." The data said "noisy." This is the core problem with LLM-generated analysis: **the failure mode isn't gibberish — it's plausible-sounding wrongness wrapped in confident language.** Without explicit rules for which evidence to trust when sources conflict, you default to whichever narrative sounds best.

This problem appears wherever an LLM produces both a summary and the underlying data — compliance auditing, code review, legal analysis. The surface is always more polished than the substance.

### 2. Not all models fail the same way

Haiku was fast and cheap, but its client-location mappings were full of noise — test files, ABI wrappers, helper utilities that had nothing to do with the actual protocol logic. Opus and Sonnet were much stronger but still produced obligations where the requirement itself was debatable.

The useful insight isn't "Opus is better than Haiku." It's that **different models have different error signatures**, and you need to know your model's specific failure pattern, not just its benchmark score.

### 3. You can't compare runs by row ID

I assumed you could compare two runs by matching obligation IDs. You can't. The same model, same EIP, same config will produce different obligation IDs between runs. The numbering drifts. If you diff by ID, you get false disagreements everywhere.

This is a subtle trap: it *looks* like rigorous comparison, but the units don't correspond. Statement-level semantic matching is required instead.

### 4. "All fields filled" means nothing

One of the built-in summary metrics was field population: what percentage of columns are filled in the output CSV? Some runs hit 100%. That sounds great until you check what's in those fields and find wrong spec locations, irrelevant client paths, and hallucinated code flows.

**Completion is process telemetry. It is not quality evidence.** This applies to any AI-assisted workflow, not just protocol verification.

### 5. Some requirements are genuinely contested

One obligation — OBL-030 for EIP-1559 — became my canonical example. The mapping mechanics looked perfectly coherent. The model found spec locations, client code, traced the flow. But the requirement itself might not actually be supported by the spec text. The *obligation extraction* was the problem, not the *obligation mapping*.

No amount of downstream accuracy fixes an upstream classification error. These need a `disputed` label, not silent inclusion in a compliance report.

---

## What Actually Improved

If correctness didn't improve dramatically, what did?

**Inspectability.** Not as a vague aspiration, but as a concrete evidence governance system that evolved over five iterations. Here's what it actually looks like.

### The three-tier evidence hierarchy

The single most important design decision was establishing which evidence wins when sources disagree:

- **Tier 1 (strongest): raw run artifacts.** The actual CSVs, model transcripts, prompts, and phase outputs. These are the ground truth.
- **Tier 2: validation documents.** Row-level scoring with rubric-based adjudication against source code.
- **Tier 3 (weakest): narrative summaries.** README prose, run summaries, and any retrospective commentary.

When tiers conflict — and they do, constantly (see CTR-001 above) — the strongest tier wins: Tier 1 overrides Tier 2 overrides Tier 3. This single rule prevents the most common failure mode in AI-assisted analysis: confident narrative overriding contradictory evidence.

### The scoring rubric

Every obligation mapping is scored on five dimensions, each rated 0–2:

1. **Statement fidelity** — does the extracted obligation match what the EIP actually says?
2. **Spec location validity** — does the cited spec code actually implement this obligation?
3. **Client location validity** — is the cited client code implementation-relevant, or noise (test files, ABI wrappers)?
4. **Flow plausibility** — does the code-flow narrative actually connect entrypoint to enforcement?
5. **Evidence sufficiency** — is there enough artifact-level evidence to adjudicate this claim?

Total score (0–10) maps to labels: `valid` (≥8), `partial` (5–7), `invalid` (≤4), or `disputed` (requirement itself is contested, regardless of score). The [full rubric](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/scoring_rubric.md) includes adjudication procedures and known pitfalls.

This matters because it replaces "looks plausible" with a structured, repeatable judgment process. Two reviewers scoring the same obligation against the rubric should converge. Without it, evaluation is subjective and unreproducible.

### The contradiction register

Contradictions between artifacts are not bugs to suppress — they're [first-class workflow objects](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/contradictions.csv). Each entry gets an ID, a description of the conflict, and a resolution rule. The register currently tracks eight contradictions (CTR-001 through CTR-008), each representing a case where two artifacts from the same system make incompatible claims.

Without a register, teams default to ignoring whichever artifact is less convenient.

### The claim ledger

The [evidence ledger](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/evidence_ledger.md) ties public-facing claims to supporting evidence, a confidence tag, and — critically — any known counterevidence. Claims in this post, for example, are backed by ledger entries. If evidence weakens, the confidence downgrades. If counterevidence emerges, it's recorded next to the claim, not buried.

This is what "discipline" means concretely: every claim has a paper trail, every confidence level has criteria, and downgrading a claim when evidence weakens is a required workflow step, not a judgment call.

None of this made the LLM smarter. All of it made the LLM's errors *findable* — and made the humans accountable for what they chose to do with those errors.

---

## The Numbers That Matter

### Per-model performance (47 direct-adjudication rows)

| Model | Rows | Avg Score (/10) | Valid | Follow-up needed |
|---|---:|---:|---:|---:|
| Opus | 20 | 9.4 | 80% | 20% (4 rows) |
| Sonnet | 12 | 9.0 | 92% | 8% (1 row) |
| Haiku | 15 | 5.0 | 13% | 87% (13 rows) |

**38.3% of all direct-adjudication rows required manual follow-up** (18/47) — but 72.2% of that burden came from Haiku outputs (13 of 18 follow-up rows). Without Haiku, follow-up drops to 15.6% (5/32).

The aggregate isn't the whole story. Governance exposed a model-tier asymmetry: Haiku-tier output is triage-grade, while claim promotion requires stronger-model adjudication. Model choice is itself a governance decision, and the evidence infrastructure made that visible.

### Why Opus is the default

The tool defaults to Opus. Sonnet scored comparably (9.0 vs 9.4) with a lower follow-up rate on our sample, but on a smaller set (12 vs 20 rows). Opus was tested more extensively against EIP-1559's complex codebase and showed the most consistent mapping quality at scale. Sonnet may well match or exceed Opus with a larger sample — we don't have enough data to say definitively — but Opus is the safer default given current evidence.

Haiku's numbers disqualify it for anything but bulk triage pre-screening.

---

## Running in CI: Why It Matters

The tool doesn't just run locally. It ships as a [reusable GitHub workflow](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40/.github/workflows) with single-run and batch-mode triggers. You can verify one EIP or an entire fork's worth of EIPs in parallel.

This was a deliberate design choice, not a feature checkbox.

**For security tooling, CI is the right deployment surface.** The inputs are fixed (EIP number, fork, client version, model), which substantially reduces the prompt-surface attack vector — no user-editable prompts, no interactive sessions. The agent operates on a shallow-cloned repo with bounded conversation turns. Every run produces an immutable artifact bundle.

Compare this to a chatbot interface where a developer might edit prompts, re-run selectively, and keep only the results they like. In protocol security, that flexibility is a liability. You want a pipeline that produces the same artifact structure every time, and you want the artifacts to be immutable evidence, not conversation history.

---

## Is This Promising? Yes — With Caveats

Let me make the affirmative case directly, since the data supports it.

**Opus at 80% valid with a 20% follow-up rate is operationally useful today.** Not for autonomous verification — but for triage acceleration. An analyst using this tool would get ~80% of their obligation mapping work pre-done, with clear flags on the remaining 20% that need human attention. That's not a replacement for expert review; it's a force multiplier for it.

### What you can defensibly claim today

> This system accelerates obligation triage and evidence collection under explicit uncertainty controls.

### What you cannot yet claim

> This system autonomously verifies protocol compliance with high confidence.

### What's missing for production readiness

1. **Deterministic pre-filters.** Simple path blocklist/allowlist rules can flag ~68% of noise rows before any human reviews them ([path-filter experiment](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/path_filter_experiment.md)). Not implemented yet.
2. **Adjudication time instrumentation.** We know the follow-up *rate* but not the follow-up *cost* in reviewer minutes. That's the real KPI for deployment.
3. **Multi-client testing.** Current evidence is geth-only. Extending to Besu, Reth, or Nethermind is mechanically straightforward (the pipeline already parameterizes the client repo) but empirically unvalidated — different languages and code structures may surface new failure modes.
4. **Expanded scored sample.** 47 direct-adjudication rows across two EIPs is enough for directional signal, not enough for hard deployment thresholds.
5. **Consensus-layer coverage.** Currently execution-specs only; consensus-specs parsing is deferred.

---

## Beyond Ethereum: Why This Pattern Generalizes

The specific application is Ethereum protocol verification. But the patterns we found likely transfer to many analogous domains where an LLM is used to analyze compliance, verify implementations, or produce structured security assessments:

- **Auditability improves faster than correctness.** Invest in making errors findable before investing in making errors rare.
- **Evidence governance is the bottleneck, not generation quality.** When a model produces both a summary and the supporting data, someone has to decide which one to trust when they disagree.
- **Cost-to-trust is the real metric, not cost-to-generate.** Our measured API cost for a single-EIP Opus run was [$4.39](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/examples/README.md); at scale with larger token budgets, template projections range $24–40 per run. Reviewer time is the dominant cost driver, and it's heavily model-tier concentrated: 72.2% of our follow-up burden came from Haiku outputs. Governance made this asymmetry visible and actionable.
- **CI deployment reduces a major class of reliability concerns.** Fixed inputs, reduced prompt surface, immutable artifacts, bounded agent scope. For deterministic workflows, this is the practical sweet spot.

If you're building LLM-assisted verification in any context — regulatory compliance, codebase auditing, specification checking — the [twelve-step methodology](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/research_working_note/essay_methodology.md) and the [evidence ledger pattern](https://github.com/petroslamb/eth-llm-poc/blob/ca15d40/docs/evaluations/evidence_ledger.md) are probably the most reusable contributions from this project.

---

## Three Predictions

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

The strongest contribution of this project isn't a claim that verification is solved. It's a workflow that got better at exposing where it might be wrong.

In protocol security — and in many domains where AI-generated analysis must be trusted — that's the maturity signal that matters.

*Evidence links in this post are pinned to commit [`ca15d40`](https://github.com/petroslamb/eth-llm-poc/tree/ca15d40).*
