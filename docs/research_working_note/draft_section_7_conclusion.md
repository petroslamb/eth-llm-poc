# VII. Conclusion: Reliability Claims Over Capability Claims

The easiest story to tell about LLM-assisted code verification is a capability story:

- models are getting better,
- context windows are getting larger,
- results look increasingly polished.

This project supports a different and more useful story.

The core bottleneck is trustworthiness.

Across runs and iterations, the most meaningful progress was not that outputs became universally correct. The meaningful progress was that outputs became easier to challenge, compare, and adjudicate.

That is why the strongest contribution of this work is methodological:

> We improved the ability to prove ourselves wrong.

---

## What Is Strongly Supported Now

1. Model choice changes failure profile materially in sampled evidence.
2. Obligation IDs are unstable; statement-level alignment is required.
3. Completion metrics can mask correctness issues.
4. Some obligations are semantically disputed and should be labeled as such.
5. Environment metadata can change interpretation of findings.

These are not abstract observations. They are grounded in concrete artifacts and contradiction handling procedures documented in the proof pack.

---

## What Is Not Proven Yet

1. Formal precision/recall/F1 at system scale.
2. Architecture-ceiling claims with numeric certainty.
3. Universal approach ranking across all tooling paradigms.
4. Autonomous, low-risk protocol verification.

This boundary is not a weakness. It is the minimum standard for honest technical reporting.

---

## Practical Thesis

If you cannot trace a claim, score it, and resolve contradictions around it, you do not have a verification system. You have a high-throughput narrative system.

In protocol security, that distinction is decisive.

The path forward is not rhetorical optimism. It is disciplined evidence governance:
- source hierarchy,
- contradiction registers,
- obligation-level scoring,
- confidence-tagged claims,
- environment-aware interpretation.

Teams that adopt this posture will produce fewer spectacular claims and more durable results.

---

## Falsifiable Near-Term Predictions

1. Teams that measure adjudication burden will ship more reliable workflows than teams measuring token cost alone.
2. Pipelines with explicit `disputed` labeling will reduce expensive false confidence incidents in review cycles.
3. Artifact-first reporting standards will become a differentiator for credible LLM verification tooling.

These predictions are intentionally operational. They can be tested with run history and review workload metrics.

---

## Final Note

The trustworthiness gap is not an argument against using LLMs in protocol security.

It is an argument for using them under stricter epistemic controls than most current tooling assumes.

That shift is not glamorous, but it is how verification systems become dependable.
