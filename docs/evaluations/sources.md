# Source Material Map: "The Trustworthiness Gap in LLM Protocol Verification"

## How to Read This File
This is a claim-oriented source map, not a general bibliography.

Each claim includes:
- **Confidence:** High / Medium / Hypothesis
- **Primary evidence paths**
- **Counterevidence paths** (if present)
- **Interpretation boundary** (what the evidence supports and what it does not)

---

## Evidence Hierarchy (Canonical)

1. **Tier 1 (Primary):** Raw CSV artifacts, manifests, prompts, phase outputs.
2. **Tier 2 (Supporting):** Evaluation summaries and run summaries.
3. **Tier 3 (Narrative):** README and retrospective prose.

Use higher tier sources to resolve contradictions in lower tiers.

---

## Claim Ledger

### Claim A: Model selection changes error profile materially in EIP-1559 runs
**Confidence:** High (qualitative + artifact inspection)

**Primary evidence:**
- `poc5/docs/QUALITATIVE_EVALUATION.md`
- `poc5/examples/qualitative_validation_transcript.md`
- `poc5/examples/runs/20260128_192948/.../phase2B_runs/20260128_234802/client_obligations_index.csv`
- `poc5/examples/runs/20260129_125052/.../phase2B_runs/20260129_130116/client_obligations_index.csv`
- `poc5/examples/runs/20260129_133849/.../phase2B_runs/20260129_135408/client_obligations_index.csv`

**Counterevidence:**
- `poc5/examples/runs/20260129_125052/.../phase2B_runs/20260129_130116/README.md` (claims full compliance despite known noise concerns elsewhere)

**Interpretation boundary:**
- Supported: model runs differ significantly in practical mapping quality.
- Not supported: exact precision/recall deltas without scoring protocol.

---

### Claim B: Obligation IDs are unstable; statement-level alignment is required
**Confidence:** High

**Primary evidence:**
- `poc5/docs/QUALITATIVE_EVALUATION.md` (explicitly notes ID instability)
- `poc5/examples/qualitative_validation_transcript.md`
- `poc4_7/notes/generated/20260129_125052/.../old_vs_new_qualitative_compare.csv`

**Interpretation boundary:**
- Supported: ID-based diffs are unreliable.
- Not supported: uniqueness of best match without ambiguity handling.

---

### Claim C: Structured phase boundaries improved auditability/replay properties
**Confidence:** Medium-High

**Primary evidence:**
- `poc4_7/README.md`
- `poc5/docs/POC_IMPLEMENTATION_SPEC.md`
- `poc5/examples/workflow_runs/21571909617/verification-report-7702/summary.md`

**Supporting context:**
- `poc5/docs/proposal/TECHNICAL_ARCHITECTURE_AND_DESIGN.md`
- `poc5/docs/proposal/summary/PROPOSAL_SUMMARY.md`

**Interpretation boundary:**
- Supported: pipeline creates inspectable artifacts with clear phase lineage.
- Not supported: phase boundaries alone guarantee correctness.

---

### Claim D: "Complete output" metrics do not guarantee semantic correctness
**Confidence:** High

**Primary evidence:**
- High field-population summaries in run summaries:
  - `poc5/examples/workflow_runs/21571909617/verification-report-7702/summary.md`
  - `poc5/examples/workflow_runs/21570420032/verification-report-7702/summary.md`
- Contradictory quality findings in:
  - `poc5/docs/QUALITATIVE_EVALUATION.md`
  - `poc5/examples/qualitative_validation_transcript.md`

**Interpretation boundary:**
- Supported: completion is a weak proxy for correctness.
- Not supported: universal failure rate from these runs.

---

### Claim E: Environment metadata can flip run interpretation
**Confidence:** High

**Primary evidence:**
- `poc5/examples/README.md`
- `poc5/examples/workflow_runs/21570420032/verification-report-7702/summary.md`
- `poc5/examples/workflow_runs/21571909617/verification-report-7702/summary.md`

**Interpretation boundary:**
- Supported: client ref/context materially affects findings.
- Not supported: broad model ranking independent of environment.

---

### Claim F: Cost templates are useful but overestimate some cached real runs
**Confidence:** High

**Primary evidence:**
- Template assumptions:
  - `poc5/docs/proposal/BUDGET_AND_COST_STRUCTURE.md`
- Real usage snapshot:
  - `poc5/examples/workflow_runs/21570420032/claude_api_cost_2026_02_01_to_2026_02_01.csv`
  - `poc5/examples/workflow_runs/21570420032/claude_api_tokens_2026_02.csv`

**Interpretation boundary:**
- Supported: caching can materially reduce effective run cost.
- Not supported: generalized monthly cost reduction factor.

---

### Claim G: Negative results are present and now partially structured
**Confidence:** Medium-High

**Primary evidence:**
- `poc4/README.md`
- `poc4_5/POC4_5_FLOW.md`
- `poc/docs/SPIKE.md`
- `poc5/docs/proposal/TECHNICAL_ARCHITECTURE_AND_DESIGN.md`

**Supporting artifact:**
- `docs/evaluations/approach_decision_log.csv`

**Interpretation boundary:**
- Supported: multiple approaches were tried and later deprioritized/rejected, with consolidated stop-condition summaries.
- Not supported: strict comparative benchmark without standardized quantitative stop criteria.

---

## Claims to Avoid (Current Evidence Insufficient)

1. "~85% transformer ceiling" for obligation extraction.
2. "3x performance" as a quantitative statement.
3. Any formal precision/recall/F1 values without published rubric and adjudicated ground truth.
4. Deterministic predictions about market standardization timelines.

---

## Current Proof-Pack Artifacts

1. `docs/evaluations/evidence_ledger.md`
- claim-by-claim mapping with confidence and counterevidence.

2. `docs/evaluations/contradictions.csv`
- explicit conflict tracking and resolution notes.

3. `docs/evaluations/scoring_rubric.md`
- obligation-level adjudication criteria.

4. `docs/evaluations/sample_scored_run.csv`
- expanded reproducible scored sample (81 rows).

5. `docs/evaluations/metrics_summary.md`
- computed model/eip summaries with limits and caveats.

6. `docs/evaluations/approach_decision_log.csv`
- normalized abandonment/selection rationale with retained lessons.

7. `docs/evaluations/path_filter_experiment.md`
- deterministic path-gating triage experiment and limits.

8. `docs/evaluations/future_work.md`
- explicit run-dependent items deferred from current publication cut.

---

## Minimal Citation Set for the Essay Body

If space is tight, prioritize these files:
1. `poc5/docs/QUALITATIVE_EVALUATION.md`
2. `poc5/examples/qualitative_validation_transcript.md`
3. `poc5/docs/POC_IMPLEMENTATION_SPEC.md`
4. `poc5/examples/workflow_runs/21570420032/verification-report-7702/summary.md`
5. `poc5/examples/workflow_runs/21571909617/verification-report-7702/summary.md`
6. `poc5/docs/proposal/BUDGET_AND_COST_STRUCTURE.md`
7. `poc4_7/notes/generated/20260129_125052/.../old_vs_new_qualitative_compare.csv`
8. `docs/evaluations/approach_decision_log.csv`
9. `docs/evaluations/path_filter_experiment.md`
10. `docs/evaluations/future_work.md`

---

## Source Hygiene Rules

1. Prefer Tier 1 artifacts when available.
2. When sources conflict, report conflict explicitly.
3. Label interpretation vs observation in draft prose.
4. Never convert qualitative language into numeric claims implicitly.
5. Keep path references exact for auditability.
