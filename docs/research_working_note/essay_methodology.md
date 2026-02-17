# Essay Methodology (Step-by-Step)

## Purpose
This document explains, in detail, the method used to produce the essay package in the evaluations and research working note folders.

Scope of this method:
- Build a publishable narrative grounded in repository evidence.
- Avoid unsupported claims.
- Make every strong claim traceable to artifacts.
- Separate current evidence from run-dependent future work.

---

## Step 1: Define the Core Thesis Constraint
1. Start from the user requirement: high-rigor, non-superficial, proposal assumptions challenged.
2. Replace capability-first framing with trustworthiness-first framing:
   - focus on falsifiability, evidence governance, contradiction handling, adjudication burden.
3. Set red-line constraints:
   - no precision/recall/F1 claims without benchmark-grade data,
   - no architecture ceiling claims without controlled evidence,
   - no "full compliance" language without row-level adjudication.

Primary outputs:
- `docs/research_working_note/outline.md`
- `docs/research_working_note/draft_section_1_introduction.md`

---

## Step 2: Build an Evidence Hierarchy Before Writing Findings
1. Inventory source artifacts across runs, workflow outputs, validation notes, and proposal docs.
2. Establish source precedence to resolve conflicts:
   - Tier 1: raw run artifacts (CSV/manifests/prompts/phase outputs)
   - Tier 2: evaluation/validation reports
   - Tier 3: narrative summaries and README prose
3. Require higher-tier evidence to override lower-tier narrative claims.

Primary outputs:
- `docs/evaluations/sources.md`
- `docs/research_working_note/draft_section_2_system_and_evidence.md`

---

## Step 3: Extract and Track Contradictions Explicitly
1. Detect claim conflicts across overlapping artifacts.
2. Record each contradiction in a structured register with resolution status and note.
3. Treat contradictions as first-class evidence, not editorial cleanup.

Primary output:
- `docs/evaluations/contradictions.csv`

Examples tracked:
- "full compliance" vs noisy row-level mappings,
- sparse gap flags vs low quality,
- disputed OBL-030 status,
- environment-sensitive EIP-7702 interpretation.

---

## Step 4: Create a Reproducible Scoring Protocol
1. Define an obligation-level rubric with fixed dimensions:
   - `statement_fidelity`
   - `spec_location_validity`
   - `client_location_validity`
   - `flow_plausibility`
   - `evidence_sufficiency`
2. Use fixed labels:
   - `valid`, `partial`, `invalid`, `disputed`
3. Keep confidence separate from score (`high`, `medium`, `hypothesis`).

Primary output:
- `docs/evaluations/scoring_rubric.md`

---

## Step 5: Build a Claim Ledger and Claim Audit Gate
1. Create a ledger where each strong claim has:
   - confidence,
   - status (`supported`/`inference`/`contested`),
   - evidence refs,
   - counterevidence when applicable.
2. Add a claim-audit file to verify draft claims map to ledger IDs.
3. Treat unmapped strong claims as blocked until evidence is added or phrasing is downgraded.

Primary outputs:
- `docs/evaluations/evidence_ledger.md`
- `docs/evaluations/claim_audit.md`

---

## Step 6: Create the Initial Scored Sample (Direct Adjudication)
1. Score direct transcript/code-backed obligations first.
2. Preserve disputed obligations explicitly instead of forcing binary labels.
3. Compute metrics only from explicit scored rows.

Primary outputs:
- `docs/evaluations/sample_scored_run.csv` (initial block)
- `docs/evaluations/metrics_summary.md` (initial block)

---

## Step 7: Expand the Dataset with Labeled Confidence Boundaries
1. Expand from 42 to 81 rows.
2. Add compare-derived rows from cross-run qualitative compare artifacts.
3. Mark compare-derived rows as `medium` confidence proxy evidence.
4. Keep clear split:
   - direct adjudication rows,
   - compare-derived rows.
5. Recompute metrics and explicitly document limitations.

Primary outputs:
- `docs/evaluations/sample_scored_run.csv` (81 rows)
- `docs/evaluations/metrics_summary.md` (expanded)

Method boundary:
- Compare-derived rows are used for trust-risk signals and triage insights, not as full substitutes for manual adjudication.

---

## Step 8: Add Operational Evidence Artifacts
1. Normalize abandonment rationale into a structured decision log.
2. Run a deterministic path-filter triage experiment on compare block.
3. Use these artifacts to strengthen operational claims (with caveats).

Primary outputs:
- `docs/evaluations/approach_decision_log.csv`
- `docs/evaluations/path_filter_experiment.md`

---

## Step 9: Draft Full Narrative, Then Create Working-Note Cut
1. Build full argument draft with complete technical anchors:
   - `docs/research_working_note/full_draft_research_working_note.md`
2. Remove stitched-draft artifacts and repetition.
3. Add compact evidence table and operating-loop diagram.
4. Produce a reader-facing working-note cut with reduced path clutter and explicit methods note:
   - `docs/research_working_note/research_working_note.md`
5. Add a working-note bundle helper:
   - `docs/research_working_note/research_working_note_bundle.md`

---

## Step 10: Separate Run-Dependent Claims into Future Work
1. Identify claims that cannot be closed without new controlled runs.
2. Move them out of current-evidence claims into explicit deferred work.
3. Keep this boundary visible in ledger, audit, metrics, and publish draft.

Primary output:
- `docs/evaluations/future_work.md`

Deferred items:
- controlled baseline vs filter rerun,
- measured minutes-per-obligation,
- balanced compare expansion across model families.

---

## Step 11: Apply Final QA Checks Before Each Commit
1. Consistency checks:
   - counts in draft == counts in metrics == counts in scored CSV.
2. Claim-boundary checks:
   - all strong claims mapped in `claim_audit.md`.
3. Format checks:
   - ASCII-clean output where practical.
4. Scope checks:
   - stage only intended the evaluations and research working note folders files.

---

## Step 12: Commit in Evidence-Coherent Increments
The work was committed in stages to preserve traceability:
1. Initial essay material snapshot.
2. Thesis rewrite around trustworthiness gap.
3. Proof-pack introduction.
4. Section expansion and claim audit integration.
5. Merged full draft.
6. Publish polish and future-work separation.

Each commit kept the essay package internally consistent at that stage.

---

## Practical Replication Checklist
If you repeat this methodology on another repo:
1. Set claim red lines first.
2. Define source hierarchy before writing conclusions.
3. Build contradiction register early.
4. Use fixed scoring rubric and confidence tags.
5. Maintain claim ledger + claim audit gate.
6. Separate direct adjudication from proxy scoring.
7. Keep run-dependent claims in explicit future work.
8. Publish only what is currently evidence-supported.
