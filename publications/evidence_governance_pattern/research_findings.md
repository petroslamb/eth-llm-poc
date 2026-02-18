# Research Findings from Prioritized Paper Review

This memo synthesizes the prioritized reading set in `papers/` and translates it into concrete guidance for the evidence-governance article draft.

Scope note:
- Sources reviewed are the local markdown conversions in `papers/`.
- This document focuses on transferable ideas, validation anchors, and overclaim risks.

## Executive Summary

The strongest support for this article's thesis is now clear:

1. The article is strongest when framed as an answer to a cost problem, not just an accuracy problem.
The paper *From Fluent to Verifiable* argues that once generation gets cheap, verification effort becomes the bottleneck ("the real cost is tracing"). This directly supports your "doesn't scale without reviewer time" section and gives it a formal structure.

2. Your five-component pattern aligns with multiple independent technical lines.
- Claim decomposition + per-claim verdicts: supported by *MedRAGChecker*.
- Conflict handling as a first-class workflow object: supported by *Rethinking All Evidence*.
- Claim promotion only after machine-checkable evidence: supported by *EviBound*.
- Evidence hierarchy concept: supported by *Med-R2* and EBM literature.

3. The paper set also sharpens your caveats.
- Confidence is not reliability (*Trust Me, I'm Wrong* / CHOKE).
- Governance artifacts can degrade into paperwork if not tied to real decisions (*BIG Argument* safety-case caution).
- Reporting context matters for external trust (*Audit Cards*).

Bottom line:
Your proposed pattern is not isolated or ad hoc. It is a coherent synthesis across claim-level verification, conflict-aware reasoning, and operational governance. The main opportunity now is to formalize "audit effort" and reduce any wording that implies proven cross-domain generalization without experiments.

Update after additional paper intake:
SOPBench adds direct empirical support for your "operating loop" argument: strong general models still fail procedural compliance when they must follow domain-specific constraints in tool-calling trajectories. This is a direct justification for explicit governance loops and release gates rather than relying on aggregate capability scores.

## Paper-by-Paper Findings (What to Use, What to Avoid)

## 1) From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents (highest priority)

Key transferable ideas:
- Frames auditability as the dominant bottleneck once report generation is cheap.
- Proposes the AAR view with four measurable properties:
  - provenance coverage
  - provenance soundness
  - contradiction transparency
  - audit effort
- Defines a strong criterion: verification effort should be much lower than generation effort (`E_verify << E_generate`).

How this helps your article:
- Upgrades Section 6 ("doesn't scale") from intuition to a structured economic claim.
- Lets you introduce "audit effort" as a first-class metric in your own loop.

Overclaim risk:
- Do not claim you implemented full provenance-graph formalism unless you actually did.
- Safe phrasing: "inspired by AAR-style properties" or "compatible with this measurement lens."

## 2) MedRAGChecker

Key transferable ideas:
- Decompose long-form output into atomic claims.
- Assign per-claim verdicts (`ENTAIL`, `NEUTRAL`, `CONTRADICT`) with calibrated confidence.
- Use multi-signal verification (textual NLI + structured KG signal) instead of single-signal pass/fail.
- Aggregate claim decisions into answer-level diagnostics (faithfulness, contradiction/hallucination rate, safety-critical error).

How this helps your article:
- Gives technical justification for claim ledger granularity and rubric dimensions.
- Supports moving from binary "works/doesn't work" judgments to layered diagnostics.

Overclaim risk:
- The paper explicitly notes teacher-label noise and dependence on teacher model choices.
- Do not present this as "objective truth extraction." Present as "higher-resolution diagnostics under explicit assumptions."

## 3) Rethinking All Evidence (CARE-RAG)

Key transferable ideas:
- Conflict module outputs:
  - binary conflict flag (`delta_c`)
  - natural-language conflict rationale (`r_c`)
- Conflict report is fed into synthesis instead of suppressing disagreement.

How this helps your article:
- Strong validation for contradiction register design.
- Suggests adding a mandatory rationale field for each contradiction entry, not just "open/resolved."

Overclaim risk:
- CARE-RAG is a RAG architecture paper; your process is governance-first.
- Keep framing as conceptual alignment, not direct architectural equivalence.

## 4) Evidence-Bound Autonomous Research (EviBound)

Key transferable ideas:
- Dual-gate governance pattern:
  - pre-execution approval gate (contract/schema validity)
  - post-execution verification gate (artifacts/metrics exist and match)
- Claims only propagate with machine-checkable evidence.
- Provides an operational "no evidence, no promotion" enforcement concept.

How this helps your article:
- Strong support for release gating in your claim ledger.
- Good anchor for "governance is architectural, not prompt-level."

Overclaim risk:
- Do not copy performance claims unless you reproduce comparable tests.
- Use design pattern, not benchmark parity, as your main link.

## 5) Med-R2

Key transferable ideas:
- Explicit hierarchy-of-evidence handling under conflict.
- Lower-level evidence can be filtered when conflicting with higher-level evidence.

How this helps your article:
- Validates your tiered evidence hierarchy with a concrete implementation precedent.
- Helps justify deterministic tie-break rules when artifacts conflict.

Overclaim risk:
- Med-R2 is biomedical-domain and retrieval-heavy; do not imply direct transfer guarantees to protocol-security mapping.

## 6) The BIG Argument for AI Safety Cases

Key transferable ideas:
- Safety case = structured argument supported by evidence in context.
- Balanced/Integrated/Grounded framing helps position your pattern as part of broader assurance practice.
- Important warning: safety cases can become paperwork without the right operational mindset.

How this helps your article:
- Strengthens "why artifact-level evidence matters" in the Gap section.
- Adds credibility language for professional and regulatory audiences.

Overclaim risk:
- Do not claim your workflow is a full safety case; it is a focused artifact-level component.

## 7) Trust Me, I'm Wrong

Key transferable ideas:
- Identifies high-certainty hallucinations even when models can answer correctly in nearby settings (CHOKE framing).
- Supports the claim that fluent confidence cannot be your trust signal.

How this helps your article:
- Reinforces the opening problem statement ("confident contradiction" is expected behavior, not an anomaly).

Overclaim risk:
- Keep examples illustrative unless you run CHOKE-like analysis on your own dataset.

## 8) Audit Cards

Key transferable ideas:
- Reporting should include context, not just scores.
- Useful template dimensions: auditor identity, scope, methodology, resources/access, process integrity, review mechanisms.
- Cross-cutting principles: justifications, assumptions, limitations.

How this helps your article:
- Suggests a final external-facing artifact that summarizes governance decisions without exposing raw internals.
- Useful for your adoption section as a practical output format.

Overclaim risk:
- Do not position audit cards as claim-level verification itself; it is reporting infrastructure around evaluation.

## Concrete Insertions for Your Current Draft

## Section 1 (The Problem)
- Add one sentence that confidence and correctness decouple in practice (anchor: CHOKE work).
- Add one sentence that the bottleneck is tracing and verification effort, not text generation (anchor: Fluent->Verifiable).

## Section 2 (Gap)
- Distinguish three layers clearly:
  - capability benchmarks (model performance)
  - governance frameworks (policy/process)
  - artifact-level claim auditability (your focus)
- Use BIG + Audit Cards to show current process-level movement, then state the remaining claim-level operations gap.

## Section 3 (Five Components)
- For contradiction register: include both conflict flag and rationale field.
- For claim ledger: consider tri-state claim status (supported/uncertain/contradicted) instead of binary.
- For rubric: mention that multi-signal verification can reduce false confidence compared with single-signal checks.

## Section 4 (What Changed)
- Add an "audit effort" subsection:
  - current observed reviewer burden (your measured manual-follow-up ratio)
  - target direction (reduce tracing time per claim over iterations)

## Section 5 (Adoption Steps)
- Add explicit gate language:
  - Gate A: schema/contract checks before execution
  - Gate B: artifact verification before claim release
- Add optional "publish an audit card summary" step for external readers.

## Section 6 (Doesn't Solve)
- Include explicit limits:
  - does not improve base model truthfulness
  - does not eliminate expert adjudication
  - can become bureaucracy if not tied to enforcement decisions
  - portability beyond your environment remains to be tested

## New Ideas Worth Considering for the Repo/Process

1. Add an `audit_effort_minutes` (or proxy step-count) field per adjudicated claim.
2. Extend contradiction rows with `conflict_rationale` and `resolution_evidence`.
3. Add `obsolescence_criteria` to ledger entries (when a prior claim should be re-audited).
4. Generate an `audit_card.md` artifact from ledger + contradiction register for external publication.
5. Track "claim promotion latency" (time from low-confidence to promoted confidence) as an operational KPI.

## Claim Safety Matrix (for Writing Discipline)

High-confidence claims you can make now:
- Existing benchmarks/frameworks leave an artifact-level trust gap in day-to-day claim adjudication.
- Claim-level governance components (hierarchy + rubric + contradiction tracking + ledger + gates) are feasible and operationally useful.
- Reviewer effort remains a core limiting factor and should be treated as a measured variable.

Claims that must stay qualified:
- "Portable to any tool-using LLM" -> say "likely portable, untested across systems."
- "Generalizes to other chains/domains" -> say "plausible, requires direct replication."
- "Improves correctness" -> avoid unless you have controlled before/after evidence on correctness itself.

## Deep Dive Status

Completed in this pass:

1. `from_fluent_to_verifiable.md`
2. `medragchecker.md`
3. `evidence_bound_autonomous_research.md`
4. `audit_cards.md`
5. `sopbench.md`

## Deep Dive Addendum (Insert-Ready)

## A) From Fluent to Verifiable: What materially strengthens your article

Core additions from the deep read:
- The paper formalizes your strongest argument as an economics constraint: generation gets cheap, but verification effort becomes the bottleneck and hidden cost.
- It gives a concrete measurement scaffold (AAR) with four properties your current workflow can map to directly:
1. `PCov` (provenance coverage): which claims have complete traceable paths.
2. `PSnd` (provenance soundness): which cited evidence actually entails the claims.
3. `CTran` (contradiction transparency): which detected conflicts are explicitly surfaced.
4. `AEff` (audit effort): average expert effort to verify claims.
- It directly supports your design principle that governance structures should reduce long-run cost, not just improve narrative quality.

Source anchors:
- `papers/from_fluent_to_verifiable.md:56`
- `papers/from_fluent_to_verifiable.md:60`
- `papers/from_fluent_to_verifiable.md:69`
- `papers/from_fluent_to_verifiable.md:872`
- `papers/from_fluent_to_verifiable.md:874`
- `papers/from_fluent_to_verifiable.md:996`
- `papers/from_fluent_to_verifiable.md:1112`
- `papers/from_fluent_to_verifiable.md:1150`

Insert-ready sentence:
- "Our aim is not only higher answer quality; it is lower verification burden per claim, so auditing remains cheaper than redoing the analysis."

Operational adaptation for your artifacts:
- Add `audit_effort_minutes` (or step-count proxy) at claim level in the evidence ledger.
- Track lightweight internal proxies for the AAR set:
1. `PCov_proxy`: ledger claims with explicit artifact links / total external claims.
2. `PSnd_proxy`: sampled claims passing row-level/line-level evidence checks.
3. `CTran_proxy`: contradictions logged / contradictions discovered in review.
4. `AEff_proxy`: mean reviewer minutes per sampled claim adjudication.

## B) MedRAGChecker: What sharpens your claim-level mechanics

Core additions from the deep read:
- The paper operationalizes claim-centric verification in a directly reusable way:
1. Decompose long-form outputs into atomic claims.
2. Assign each claim a tri-state verdict (`ENTAIL`, `NEUTRAL`, `CONTRADICT`).
3. Keep a calibrated support score, not just a class label.
4. Aggregate per-claim outcomes into answer-level diagnostics.
- It also improves rigor by combining two different signal types and explicitly tuning thresholds before freezing them across test sets.
- Their human-alignment section reports positive correlation between some diagnostics and human ratings, which supports using claim-level diagnostics as governance signals rather than raw model confidence alone.
- Important caveat from the paper itself: teacher supervision is useful but noisy; conclusions are conditional on teacher choice. This is a strong anti-overclaim anchor for your piece.

Source anchors:
- `papers/medragchecker.md:249`
- `papers/medragchecker.md:261`
- `papers/medragchecker.md:262`
- `papers/medragchecker.md:526`
- `papers/medragchecker.md:536`
- `papers/medragchecker.md:539`
- `papers/medragchecker.md:577`
- `papers/medragchecker.md:2988`
- `papers/medragchecker.md:2993`
- `papers/medragchecker.md:291`
- `papers/medragchecker.md:298`

Insert-ready sentence:
- "We treat each output as a bundle of atomic claims with tri-state outcomes and confidence, then aggregate those claim outcomes into run-level diagnostics."

Operational adaptation for your artifacts:
- Move claim ledger statuses to tri-state (`supported`, `uncertain`, `contradicted`) plus confidence.
- Add a `threshold_version` field to each scoring run so calibration choices are explicit and stable.
- Keep a `teacher_or_rule_basis` field so readers can see what verifier basis was used in each iteration.

## C) EviBound: What strengthens your operating loop and release gating

Core additions from the deep read:
- The strongest reusable structure is not their benchmark number; it is their enforcement architecture:
1. Pre-execution approval gate verifies the evidence contract schema.
2. Post-execution verification gate checks machine-queryable artifacts and status.
3. Failures route to the minimal necessary repair phase, with bounded retries.
- Their verification protocol gives a concrete check order your workflow can mirror: run identifier queryability, finished status, required artifacts, optional metric constraints.
- Their ablation progression (`100% -> 25% -> 0%` hallucination) is useful as directional evidence that dual gates outperform prompt-only and verification-only setups in their environment.
- They report modest runtime overhead (`~8.3%`) for that governance layer, which is useful as a feasibility anchor for teams worried about throughput.
- They also include useful self-limitation language you can reuse: single model family, domain-specific tasks, and human oversight still needed.

Source anchors:
- `papers/evidence_bound_autonomous_research.md:56`
- `papers/evidence_bound_autonomous_research.md:60`
- `papers/evidence_bound_autonomous_research.md:123`
- `papers/evidence_bound_autonomous_research.md:127`
- `papers/evidence_bound_autonomous_research.md:320`
- `papers/evidence_bound_autonomous_research.md:330`
- `papers/evidence_bound_autonomous_research.md:336`
- `papers/evidence_bound_autonomous_research.md:375`
- `papers/evidence_bound_autonomous_research.md:417`
- `papers/evidence_bound_autonomous_research.md:651`
- `papers/evidence_bound_autonomous_research.md:652`
- `papers/evidence_bound_autonomous_research.md:653`
- `papers/evidence_bound_autonomous_research.md:922`
- `papers/evidence_bound_autonomous_research.md:1024`
- `papers/evidence_bound_autonomous_research.md:1034`

Insert-ready sentence:
- "Our release discipline follows a dual-gate rule: validate the claim contract before execution, and validate machine-checkable artifacts before external publication."

Operational adaptation for your artifacts:
- Add an explicit `evidence_contract` block per run in your docs:
1. `run_id` (or equivalent immutable run identifier),
2. required artifacts,
3. completion status,
4. optional metric constraints.
- Add a `failure_route` field (`contract_refine`, `runtime_repair`, `evidence_regen`, `replan`) to contradiction/issue tracking.

## D) Audit Cards: What improves external trust and publication quality

Core additions from the deep read:
- The paper offers a practical external reporting format built around:
1. Three principles: justifications, assumptions, limitations.
2. Six contextual features: who, what, how, access/resources, process integrity, review mechanisms.
- Their survey of 24 reports strengthens your argument that context is systematically underreported, especially around integrity/review/obsolescence.
- The underreporting is concrete, not vague: only `4/24` detail evaluator-integrity arrangements, only `11/24` specify auditor resource access, and `0/24` explicitly report obsolescence criteria.
- Their obsolescence finding maps cleanly to your need to define when prior claims must be re-audited.

Source anchors:
- `papers/audit_cards.md:201`
- `papers/audit_cards.md:208`
- `papers/audit_cards.md:209`
- `papers/audit_cards.md:766`
- `papers/audit_cards.md:767`
- `papers/audit_cards.md:817`
- `papers/audit_cards.md:824`
- `papers/audit_cards.md:833`
- `papers/audit_cards.md:1277`
- `papers/audit_cards.md:1287`

Insert-ready sentence:
- "Beyond scores, trust depends on context: who audited, what scope was tested, what assumptions were made, what constraints applied, and how review and correction are handled."

Operational adaptation for your artifacts:
- Add `audit_card.md` per publication/release with the 3+6 structure.
- Add `obsolescence_criteria` to ledger claims (for example: upstream spec change, model change, scoring-rubric version change, artifact schema change).

## Post-Deep-Dive Priority Actions (highest ROI)

1. Add claim-level `audit_effort_minutes` and begin tracking at sample level immediately.
2. Upgrade claim ledger to tri-state outcomes with confidence and threshold version.
3. Add a dual-gate checklist to the operating loop docs (contract gate + artifact gate).
4. Publish an `audit_card.md` companion for external readers.
5. Add obsolescence criteria so claim validity is explicitly time-bounded.

## E) SOPBench: What validates your Operating Loop thesis

Core additions from the deep read:
- SOPBench directly evaluates whether agents follow procedures during tool use, not just whether they eventually complete tasks.
- It operationalizes compliance with a multi-dimensional verifier:
1. action/function permissibility,
2. database outcome matching versus oracle execution,
3. procedure completeness (required verification steps actually performed).
- This aligns exactly with your governance claim that "correct-looking outcomes are insufficient if verification steps are skipped."
- It provides a concrete scale anchor for the problem: 7 domains, 167 tools/functions, 97 services, 903 validated test cases, and over 24k trajectories.
- Empirically, the paper reports that only a small top subset of models exceed 60% pass rates, many strong models are in the 30-50% band, small models are often below 20%, and jailbreak pressure degrades adherence further.

Why this matters to your article:
- It is the missing bridge between "model capability benchmarks" and "run-level governance":
  outcome success does not guarantee procedural compliance.
- It supports your argument that governance needs explicit loop enforcement (check constraints, then act), not only stronger base models.
- It strengthens Section 5 (adoption/operating loop) with an external benchmark showing why custom SOP enforcement is necessary.

Source anchors:
- `papers/sopbench.md:49`
- `papers/sopbench.md:53`
- `papers/sopbench.md:60`
- `papers/sopbench.md:121`
- `papers/sopbench.md:130`
- `papers/sopbench.md:265`
- `papers/sopbench.md:268`
- `papers/sopbench.md:274`
- `papers/sopbench.md:290`
- `papers/sopbench.md:293`
- `papers/sopbench.md:430`
- `papers/sopbench.md:431`
- `papers/sopbench.md:433`
- `papers/sopbench.md:661`
- `papers/sopbench.md:683`
- `papers/sopbench.md:688`
- `papers/sopbench.md:778`

Insert-ready sentence:
- "Benchmark evidence now shows the core issue is procedural reliability: agents can still fail required verification steps even when they appear capable at the task level."

Operational adaptation for your artifacts:
- Add an `operating_loop_compliance` checklist per run:
1. prerequisite checks executed,
2. forbidden actions blocked,
3. final action called only after prerequisite satisfaction.
- Add a simple `constraint_following_rate` metric for scored runs:
  compliant trajectories / total trajectories sampled.
- Separate failure labels into:
1. `outcome_wrong_procedure_wrong`,
2. `outcome_correct_procedure_wrong`,
3. `outcome_wrong_procedure_correct`,
4. `outcome_correct_procedure_correct`.
This mirrors SOPBench error analysis and prevents outcome-only overestimation.

## Updated Concept-to-Paper Mapping

| Concept | Primary Paper | Borrowed Technical Detail |
|---|---|---|
| Release Gates | `evidence_bound_autonomous_research.md` | Approval + Verification gates; claims blocked unless machine-checkable evidence contract is satisfied. |
| Claim Ledger | `from_fluent_to_verifiable.md` | Claim-level auditability scaffold (`PCov`, `PSnd`, `CTran`, `AEff`) and semantic provenance framing. |
| Operating Loop | `sopbench.md` | Multi-dimensional procedural compliance checks; trajectory-level constraint adherence, not outcome-only scoring. |
| Evidence Hierarchy | `med_r2.md` | Hierarchical evidence tie-break logic under conflicts. |

## Sources Reviewed

- `papers/from_fluent_to_verifiable.md`
- `papers/medragchecker.md`
- `papers/rethinking_all_evidence.md`
- `papers/evidence_bound_autonomous_research.md`
- `papers/sopbench.md`
- `papers/med_r2.md`
- `papers/big_argument_for_ai_safety_cases.md`
- `papers/trust_me_im_wrong.md`
- `papers/audit_cards.md`
