# The Trustworthiness Gap in LLM Protocol Verification

**Evidence from Ethereum Protocol Security Research**

_Draft v1.0 - Rewritten Section I_

---

## I. Introduction: The Wrong Problem Statement

Most discussions about LLMs in software start with a capability question: 

> "Can the model do the task?"

In protocol security, that is the wrong first question.

The first question should be:

> "Can we trust and falsify what the model claims it found?"

That distinction sounds subtle. In practice, it is the difference between a useful verification workflow and an expensive confidence machine.

I learned this building an LLM-assisted EIP verification pipeline for Ethereum. The system extracts obligations from EIP text, maps them into execution-specs, maps them again into client code, and flags gaps. On paper, this looks like a straightforward automation problem. In reality, it exposed a deeper bottleneck: output quality is not the only variable; **output trustworthiness** is the limiting factor.

This essay argues that current LLM verification workflows fail less because they cannot generate plausible mappings, and more because teams lack disciplined ways to establish which mappings are reliable, which are disputed, and which are simply wrong.

### A Concrete Contradiction

The evidence base itself contains the warning sign.

Some artifacts describe runs as effectively complete and compliant. Other artifacts, on overlapping tasks, document high-noise client mappings, unstable obligation identities, and questionable extracted requirements. Both are "real" outputs. Both are written in professional language. Only one can be closer to ground truth per row.

This is not a minor editorial issue. It is the core systems issue.

If a verification pipeline can produce polished but conflicting narratives from nearby runs, then the engineering problem is not just inference quality. The problem is governance of evidence.

### From Capability Gap to Trustworthiness Gap

I call this the **trustworthiness gap**:

**The gap between what an LLM pipeline can produce and what a reviewer can independently validate with bounded effort.**

This framing is intentionally operational. It avoids philosophical debates about model intelligence and focuses on what matters in protocol security work:

1. Can I trace each claim to concrete code evidence?
2. Can I disprove weak claims quickly?
3. Can I reproduce the analysis and compare runs without ambiguity?

If the answer is "not reliably," then the system is not yet a verifier. It is a hypothesis generator.

That is still useful. But it must be described honestly.

### The Task Is Hard for Structural Reasons

Ethereum obligation mapping combines four difficult operations:

1. Extract atomic obligations from natural-language EIP text.
2. Locate corresponding reference implementation behavior in execution-specs.
3. Locate corresponding client implementation behavior across large codebases.
4. Determine whether differences are true gaps, ambiguity artifacts, or indexing noise.

Each step can look successful in isolation while introducing uncertainty that only appears later.

A fully populated CSV is not proof of correctness.
A plausible code flow paragraph is not proof of semantic alignment.
A clean summary is not proof of low false-positive rate.

This asymmetry is exactly why "looks good" workflows fail under audit pressure.

### What Improved, and What Didn’t

Across PoC iterations, one pattern became clear:

- **Auditability improved significantly** once the process was split into strict phase boundaries with structured artifacts.
- **Correctness improved unevenly** and remained sensitive to model behavior, prompt details, environment context, and obligation ambiguity.

This distinction matters.

Phase boundaries did not magically solve mapping accuracy. What they did do is make disagreements inspectable. They turned hidden failure into explicit records: prompts, phase outputs, CSV deltas, and rerunnable chains.

That shift is easy to undervalue. It is actually the foundation of trustworthy LLM-assisted verification.

### Why This Essay Takes a Different Angle

A common essay path here would be to make a bold architecture claim: model ceilings, hard percentages, timeline predictions.

I am deliberately not doing that as the center of argument.

The stronger and more defensible argument is this:

1. The current evidence supports a trustworthiness diagnosis more strongly than a hard capability ceiling.
2. Negative and abandoned attempts are first-class evidence, not embarrassing footnotes.
3. In security-critical workflows, design quality is measured by falsifiability and adjudication cost, not by output fluency.

This is a more conservative thesis. It is also more useful for practitioners deciding what to build now.

### Central Claims for the Full Essay

The full essay develops five claims.

1. **The dominant failure mode is evidence governance, not raw generation ability.**
LLMs can produce high-volume, high-confidence mappings faster than teams can reliably validate them.

2. **Traceable pipelines outperform opaque pipelines even when both are imperfect.**
The phase-boundary pattern improved debuggability, replayability, and dispute resolution.

3. **Model choice changes failure profile, not just apparent quality.**
Different models fail differently: noise-heavy location drift, compressed constraints, or partial flows.

4. **Contradiction handling must be built into the workflow.**
Without explicit source hierarchy and contradiction registers, teams drift toward selective interpretation.

5. **The practical KPI is cost-to-trust, not cost-per-run.**
Token pricing matters, but adjudication burden is the real scaling constraint.

### What This Essay Does Not Claim

To keep the argument clean, I explicitly avoid overreach.

This essay does **not** claim:

- formal precision/recall/F1 for the current system,
- a proven numeric architecture ceiling,
- universal model ranking independent of environment context,
- solved automation of protocol verification.

Instead, it documents where evidence is strong, where it is contested, and what engineering controls reduce trust risk now.

### Roadmap

The rest of the essay proceeds in six moves.

- **Section II** defines the system and the evidence hierarchy used to adjudicate claims.
- **Section III** examines what the runs actually show, including model-specific failure profiles and obligation instability.
- **Section IV** analyzes abandoned approaches as structured negative results.
- **Section V** proposes a verification-first design pattern centered on falsifiability.
- **Section VI** offers a practical framework for teams shipping similar tools.
- **Section VII** concludes with reliability-focused predictions and explicit falsification criteria.

### Why This Matters Beyond Ethereum

Ethereum is the case study, not the boundary.

Any team using LLMs for code auditing, compliance mapping, migration risk analysis, or safety-critical change review will face the same structural issue:

The pipeline can produce credible language faster than the organization can produce credible certainty.

That is the trustworthiness gap.

Closing it is mostly an engineering and evaluation discipline problem, not a prompt style problem.

---

_[End of Section I - Rewritten Draft]_ 

---

## Revision Notes

### What changed from the previous draft
- Replaced architecture-ceiling rhetoric with trustworthiness-focused thesis.
- Removed unsupported numeric claims.
- Elevated contradictory artifacts and source hierarchy to first-class narrative elements.
- Shifted framing from "model capability" to "evidence governance + adjudication." 

### What Section II must deliver
- Formal evidence hierarchy with examples.
- Canonical run table with environment metadata.
- Claim confidence tagging method.

### What Section III must deliver
- Artifact-first comparison, not anecdotal model commentary.
- Explicit contradiction cases and resolution logic.
- Clear boundary between observation and inference.
