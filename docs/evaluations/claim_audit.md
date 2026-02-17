# Claim Audit (Draft Sections I-VII)

Purpose: ensure every strong claim in the draft maps to an entry in `docs/evaluations/evidence_ledger.md`.

Status legend:
- `covered`: mapped to one or more ledger claims.
- `partial`: mapped, but confidence limited or caveat needed.
- `needs-ledger`: strong claim appears in draft but no explicit ledger row yet.

---

## Section Coverage

| Section file | Major claim | Ledger IDs | Status | Notes |
|---|---|---|---|---|
| `docs/evaluations/future_work.md` | Run-dependent claims are explicitly deferred and separated from current evidence claims | C013/C016 | covered | Prevents mixing no-run evidence with rerun-dependent conclusions |
| `docs/research_working_note/research_working_note.md` | Working-note cut preserves bounded trustworthiness thesis and explicit limits | C001-C016 | covered | Reduced path clutter but kept evidence boundaries and caveats |
| `docs/research_working_note/full_draft_research_working_note.md` | Final merged narrative keeps trustworthiness thesis bounded to current evidence | C001-C016 | covered | v2 merge removes unsupported ceilings and keeps explicit evidence anchors |
| `docs/research_working_note/draft_section_1_introduction.md` | Trustworthiness bottleneck dominates current evidence | C012 + C001/C003/C007 | covered | Keep phrasing as thesis/inference, not theorem |
| `docs/research_working_note/draft_section_1_introduction.md` | Contradictory artifacts exist | C003 + contradictions CTR-001/002/005 | covered | Explicitly cite contradiction rows in final merged draft |
| `docs/research_working_note/draft_section_2_system_and_evidence.md` | Phase-boundary pipeline + artifacts support auditability | C004 | covered | Avoid claiming correctness gains not evidenced |
| `docs/research_working_note/draft_section_2_system_and_evidence.md` | Strict source hierarchy is required | C003 + CTR records | covered | Methodological claim, defensible |
| `docs/research_working_note/draft_section_3_what_runs_show.md` | Model differences are error-profile differences | C001/C005/C006 + sample metrics | covered | Keep "sample" qualifier |
| `docs/research_working_note/draft_section_3_what_runs_show.md` | ID instability requires statement-level alignment | C002 | covered | Strongly supported |
| `docs/research_working_note/draft_section_3_what_runs_show.md` | Completeness metrics can mask correctness | C003 + CTR-005 | covered | Strongly supported |
| `docs/research_working_note/draft_section_3_what_runs_show.md` | OBL-030 is disputed | C007 | covered | Preserve disputed label in all summaries |
| `docs/research_working_note/draft_section_3_what_runs_show.md` | Environment context can invert interpretation | C008 | covered | Include run metadata in final narrative |
| `docs/research_working_note/draft_section_4_postmortem_of_abandoned_approaches.md` | Abandoned approaches provide useful negative evidence | C011 + C014 | covered | Keep caveat: fragmented decision trail |
| `docs/research_working_note/draft_section_4_postmortem_of_abandoned_approaches.md` | Simpler phase-boundary approach survived on debuggability | C004 + C011 + C014 | partial | Valid directionally; avoid universal claims |
| `docs/research_working_note/draft_section_5_trustworthiness_design_pattern.md` | Falsifiability-first design pattern reduces trust risk | C001-C008 synthesis | partial | Synthesis claim; keep as design recommendation |
| `docs/research_working_note/draft_section_6_builder_framework.md` | Cost-to-trust should replace cost-per-run as primary KPI | C001/C003/C009/C012 + C013 | partial | Operational recommendation; now better supported but still not benchmark-grade |
| `docs/research_working_note/draft_section_7_conclusion.md` | Reliability claims should outrank capability claims in current state | C012 + supporting set | covered | Keep explicit "current evidence" scope |

---

## Ledger Follow-Ups

Current follow-up priorities:

1. Upgrade `C013` from workload proxies to measured minutes-per-obligation (`requires new run`; see `docs/evaluations/future_work.md`).
2. Upgrade `C016` from hypothesis to supported via controlled rerun with filter-constrained generation (`requires new run`; see `docs/evaluations/future_work.md`).
3. Expand compare-derived scoring across additional models for balanced apples-to-apples analysis (`requires new run`; see `docs/evaluations/future_work.md`).

---

## Hard Rules for Final Merge Draft

1. Any sentence with numeric comparison must cite sample scope and limitations.
2. Any architecture-general sentence must be labeled as hypothesis unless benchmark-backed.
3. Any statement about abandonment rationale must reference specific artifact evidence and caveats.
4. Keep disputed obligations explicitly marked in all summary tables.
5. Compare-derived scoring rows must be labeled as medium-confidence proxy evidence, not equivalent to full manual adjudication.
