# Qualitative Evaluation (Validation Included)

This document summarizes qualitative validation performed on PoC outputs. It does not claim formal correctness; it
records what was spot-checked, what was compared across runs, and what issues were observed.

Validation was performed with `gpt-5.2-codex (high thinking)` to reduce Anthropic model bias and increase validation
diversity.

## Evidence Sources
- Qualitative validation transcript (source of truth): [examples/qualitative_validation_transcript.md](../examples/qualitative_validation_transcript.md)
- Example CI run summary (EIP-7702, Opus): [examples/workflow_runs/21571909617/verification-report-7702/summary.md](../examples/workflow_runs/21571909617/verification-report-7702/summary.md)

## Method (Qualitative Validation)
- Manual spot-checks of obligations against the EIP text, execution-specs, and geth sources.
- Cross-model comparison using statement similarity because obligation IDs are not stable across runs.
- Focused validation on a sampled subset of rows rather than exhaustive proof.

## Scope
- EIP-1559 obligation extraction and mapping (London fork), across multiple model runs.
- EIP-2930 (Berlin fork) full pipeline run with spot checks.

## Key Findings (From the Transcript)
- **Obligation IDs are not stable across runs.** Statement-similarity matching is required to compare runs reliably.
- **Haiku run (EIP-1559/London):** client locations frequently pointed to ABI/test/engine files; the 12-row sample had
  only a small number of solid matches, indicating high noise in client mapping for that run.
- **Sonnet run (EIP-1559/London):** client locations were mostly plausible and within core geth code; spec locations
  used shortened paths but resolved under execution-specs. Overall stronger than the Haiku run.
- **Opus run (EIP-1559/London):** most rows were functionally correct, but several statements were incomplete (missing
  constraints) and at least one obligation (EIP1559-OBL-030) appeared questionable relative to the spec.
- **Opus vs Sonnet comparison:** Sonnet tended to be more verbose and explicit on constraints; Opus was more concise
  and missed some constraint details. Both runs treated EIP1559-OBL-030 as a requirement despite the spec not clearly
  supporting it.
- **EIP-2930/Berlin (Opus):** spot-checked obligations (transaction type, access list shape, storage key size) matched
  the EIP text, execution-specs, and geth.

## Practical Implications
- Normalize spec paths when comparing locations (e.g., fork.py -> forks/london/fork.py).
- For client locations, prefer deterministic search (rg-based) and constrain to core geth paths to reduce drift.
- Treat any obligation that points to test/ABI/engine-api paths as suspect until independently validated.

## Example Run Mapping
- 20260128_192948 -> Sonnet
- 20260129_125052 -> Haiku
- 20260129_133849 -> Opus
- 20260129_161814 -> Opus (EIP-2930 Berlin full phase chain)

## Implications
- These outputs are best treated as high-signal hypotheses that require targeted validation, not as ground truth.
- Qualitative evaluation is used to select models, tune prompts, and prioritize follow-up checks.
- The pipeline's value is in traceability and audit-friendly artifacts; correctness is established via iterative
  validation and sampling.
