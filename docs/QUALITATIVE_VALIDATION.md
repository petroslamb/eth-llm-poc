# Qualitative Validation (Examples)

This document summarizes the qualitative validation work captured in the example transcript and example run artifacts.
It is intended as a concise, high-signal overview for reviewers who want to understand how model outputs were
validated and how the different runs compare.

## Where to look

- Transcript (source of truth for this summary):
  `examples/qualitative_validation_transcript.md`
- Example run artifacts (timestamped):
  `examples/runs/`
- Model mapping for the example runs:
  `examples/runs/README.md`

## Scope

The transcript focuses on EIP-1559 obligation extraction and mapping (London fork) across multiple model runs,
plus a later EIP-2930 (Berlin fork) run. Validation is qualitative: spot-checking a sample of obligations against execution-specs and geth sources, and comparing the coherence of spec and client locations.


## Key findings

- IDs are not stable across runs.
  - The same obligation can move to a different ID (e.g., GASPRICE moved from OBL-001 to OBL-035 in a later run).
  - Statement-similarity alignment is required for meaningful comparisons.

- Haiku run (timestamp 20260129_125052) shows substantial client-location drift.
  - Many client references land in ABI bindings, tests, or unrelated files.
  - Several spec references are “nearby” but not exact, and some statements are unsupported by the cited lines.
  - Conclusion: client location reliability is low for this run.

- Sonnet run (timestamp 20260128_192948) is materially stronger on client mappings.
  - Client references generally point to core geth code (state_transition, consensus/misc/eip1559, vm/instructions).
  - Spec paths are under-qualified (e.g., fork.py, vm/instructions/environment.py) but resolve correctly under
    `specs/execution-specs/src/ethereum/forks/london/`.

- Opus run (timestamp 20260129_133849) is mostly correct with some gaps.
  - Most sampled obligations align with both execution-specs and geth.
  - Noted issues: incomplete statements (e.g., intrinsic gas formula, gas-limit bounds) and at least one
    mis-located client check (gasUsed <= gasLimit).
  - One requirement (fork-block parent_gas_target) appears questionable in both spec and client code.

- Opus run for EIP-2930 (timestamp 20260129_161814) appears correct in spot-checks.
  - Transaction type, access list shape, and storage key size were validated against both EIP text and code.

## Practical implications

- Normalize spec paths when comparing locations (e.g., fork.py -> forks/london/fork.py).
- For client locations, prefer deterministic search (rg-based) and constrain to core geth paths to reduce drift.
- Treat any obligation that points to test/ABI/engine-api paths as suspect until independently validated.

## Example run mapping (from transcript)

- 20260128_192948 -> Sonnet
- 20260129_125052 -> Haiku
- 20260129_133849 -> Opus
- 20260129_161814 -> Opus (EIP-2930 Berlin full phase chain)

See `examples/runs/README.md` for the same mapping
