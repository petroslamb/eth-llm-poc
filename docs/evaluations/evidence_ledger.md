# Evidence Ledger

This ledger records claim-level evidence for the essay angle: **auditability improved faster than correctness**.

Legend:
- Confidence: `high`, `medium`, `hypothesis`
- Status: `supported`, `contested`, `inference`

---

## C001 — Model selection materially changes error profile in EIP-1559 runs
- Confidence: `high`
- Status: `supported`
- Evidence:
  - `poc5/docs/QUALITATIVE_EVALUATION.md:5`
  - `poc5/docs/QUALITATIVE_EVALUATION.md:35`
  - `poc5/docs/QUALITATIVE_EVALUATION.md:39`
  - `poc5/examples/qualitative_validation_transcript.md:132`
  - `poc5/examples/qualitative_validation_transcript.md:169`
  - `poc5/examples/qualitative_validation_transcript.md:209`
  - `poc5/examples/qualitative_validation_transcript.md:252`
- Counterevidence:
  - `poc5/examples/runs/20260129_125052/phase0A_runs/20260129_125052/phase1A_runs/20260129_125145/phase1B_runs/20260129_125500/phase2A_runs/20260129_125803/phase2B_runs/20260129_130116/README.md:82`
- Notes: qualitative but repeated in multiple artifacts.

## C002 — Obligation IDs are unstable; statement-level matching is required
- Confidence: `high`
- Status: `supported`
- Evidence:
  - `poc5/docs/QUALITATIVE_EVALUATION.md:26`
  - `poc5/docs/QUALITATIVE_EVALUATION.md:34`
  - `poc5/examples/qualitative_validation_transcript.md:62`
  - `poc5/examples/qualitative_validation_transcript.md:275`

## C003 — "CSV completeness" is a weak proxy for correctness
- Confidence: `high`
- Status: `supported`
- Evidence:
  - `poc5/examples/workflow_runs/21570420032/verification-report-7702/summary.md:51`
  - `poc5/examples/workflow_runs/21570420032/verification-report-7702/summary.md:62`
  - `poc5/examples/qualitative_validation_transcript.md:132`
  - `poc5/examples/qualitative_validation_transcript.md:169`
- Notes: high population can coexist with many low-quality client mappings.

## C004 — Phase boundaries improved auditability/replay structure
- Confidence: `medium-high`
- Status: `supported`
- Evidence:
  - `poc4_7/README.md:125`
  - `poc4_7/README.md:126`
  - `poc5/docs/POC_IMPLEMENTATION_SPEC.md:58`
  - `poc5/docs/POC_IMPLEMENTATION_SPEC.md:115`
- Counterevidence:
  - correctness still mixed in spot-checks (`poc5/examples/qualitative_validation_transcript.md:251`).

## C005 — Haiku EIP-1559 client mappings were often noisy/non-core in sampled validation
- Confidence: `high`
- Status: `supported`
- Evidence:
  - `poc5/docs/QUALITATIVE_EVALUATION.md:35`
  - `poc5/examples/qualitative_validation_transcript.md:103`
  - `poc5/examples/qualitative_validation_transcript.md:168`

## C006 — Opus EIP-1559 run was mostly correct but had partial/incomplete/disputed rows
- Confidence: `high`
- Status: `supported`
- Evidence:
  - `poc5/examples/qualitative_validation_transcript.md:209`
  - `poc5/examples/qualitative_validation_transcript.md:217`
  - `poc5/examples/qualitative_validation_transcript.md:226`
  - `poc5/examples/qualitative_validation_transcript.md:246`
  - `poc5/examples/qualitative_validation_transcript.md:251`

## C007 — EIP1559-OBL-030 is disputed/questionable and should not be treated as settled
- Confidence: `high`
- Status: `supported`
- Evidence:
  - `poc5/docs/QUALITATIVE_EVALUATION.md:40`
  - `poc5/examples/qualitative_validation_transcript.md:246`
  - `poc5/examples/qualitative_validation_transcript.md:307`
- Counterevidence:
  - included as an obligation in model outputs.

## C008 — Environment metadata can flip interpretation (EIP-7702 "missing" vs "clean")
- Confidence: `high`
- Status: `supported`
- Evidence:
  - `poc5/examples/README.md:30`
  - `poc5/examples/workflow_runs/21570420032/verification-report-7702/summary.md:66`
  - `poc5/examples/README.md:34`
  - `poc5/examples/workflow_runs/21571909617/verification-report-7702/summary.md:66`

## C009 — Budget templates overestimate some real runs when prompt cache is effective
- Confidence: `medium-high`
- Status: `supported`
- Evidence:
  - `poc5/docs/proposal/BUDGET_AND_COST_STRUCTURE.md:35`
  - `poc5/docs/proposal/BUDGET_AND_COST_STRUCTURE.md:56`
  - `poc5/examples/workflow_runs/21570420032/claude_api_cost_2026_02_01_to_2026_02_01.csv`
  - `poc5/examples/workflow_runs/21570420032/claude_api_tokens_2026_02.csv`

## C010 — Quantitative precision/recall/F1 are not yet established
- Confidence: `high`
- Status: `supported`
- Evidence:
  - `poc5/docs/QUALITATIVE_EVALUATION.md:14`
  - `docs/evaluations/knowledge_gaps.md:7`
  - `docs/evaluations/knowledge_gaps.md:122`

## C011 — Abandoned approaches are documented but not benchmarked with uniform stop criteria
- Confidence: `medium`
- Status: `inference`
- Evidence:
  - `poc4/README.md:24`
  - `poc4_5/POC4_5_FLOW.md:17`
  - `poc5/docs/proposal/TECHNICAL_ARCHITECTURE_AND_DESIGN.md:66`
- Notes: enough for design postmortem narrative; not enough for strict comparative benchmarking.

## C012 — The strongest defensible thesis is trustworthiness bottlenecks, not hard capability ceilings
- Confidence: `medium`
- Status: `inference`
- Evidence:
  - C001–C011 combined
  - C013–C016 (operational and triage-control evidence)
- Counterevidence:
  - no formal benchmark yet to prove alternative theses false.

## C013 — Adjudication workload is non-trivial and iterative in current practice
- Confidence: `medium-high`
- Status: `supported`
- Evidence:
  - `poc5/examples/qualitative_validation_transcript.md:90`
  - `poc5/examples/qualitative_validation_transcript.md:132`
  - `poc5/examples/qualitative_validation_transcript.md:202`
  - `poc5/examples/qualitative_validation_transcript.md:266`
  - `docs/evaluations/metrics_summary.md`
- Notes: repeated spot-check/remapping loops plus current follow-up-rate proxies (38.3% in direct-adjudication rows) indicate substantial manual review effort.
- Remaining gap: measured minutes-per-obligation still requires controlled rerun instrumentation (tracked in `docs/evaluations/future_work.md`).

## C014 — Abandoned-approach rationale is now normalized into a decision log
- Confidence: `medium-high`
- Status: `supported`
- Evidence:
  - `docs/evaluations/approach_decision_log.csv`
  - `poc4/README.md`
  - `poc4_5/POC4_5_FLOW.md`
  - `poc/docs/SPIKE.md`
  - `poc5/docs/proposal/TECHNICAL_ARCHITECTURE_AND_DESIGN.md:66`
- Notes: evidence remains partly qualitative, but stop conditions and retained lessons are now consolidated in one artifact.

## C015 — Deterministic client-path filters can flag noisy mappings as a triage control
- Confidence: `medium`
- Status: `supported`
- Evidence:
  - `docs/evaluations/path_filter_experiment.md`
  - `poc4_7/notes/generated/20260129_125052/phase0A_runs/20260129_125052/phase1A_runs/20260129_125145/phase1B_runs/20260129_125500/phase2A_runs/20260129_125803/phase2B_runs/20260129_130116/old_vs_new_qualitative_compare.csv`
  - `docs/evaluations/sample_scored_run.csv`
- Notes: in the compare block, deterministic filters flag most obvious noise-heavy rows before manual review.

## C016 — Path-filtered generation may improve final mapping quality, but controlled rerun evidence is still missing
- Confidence: `hypothesis`
- Status: `inference`
- Evidence:
  - C015
  - `poc5/docs/QUALITATIVE_EVALUATION.md:49`
  - `poc5/examples/qualitative_validation_transcript.md:124`
  - `poc5/examples/qualitative_validation_transcript.md:171`
- Counterevidence:
  - no controlled rerun in current proof pack showing measured invalid-row reduction after filter-constrained generation.
  - run-dependent requirements tracked in `docs/evaluations/future_work.md`.

---

## Usage Rules for Drafting
1. Any numeric performance claim requires a scored dataset and method note.
2. Any strong claim must cite at least one Tier-1 or Tier-2 source.
3. Contested claims must include counterevidence inline.
4. Disputed obligations (e.g., OBL-030) must be labeled explicitly in prose.
