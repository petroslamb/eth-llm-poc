# eth-llm-poc (PoC 5)

**Purpose:** First draft deliverable of the RFP. This repo packages the PoC 4.7 installable package and the PoC 4.8 reusable workflow so it can be run from any external repo without carrying execution-specs, EIPs, or client submodules.

## What’s inside

- **PoC 4.7 package**: `poc4_7/` (installable Python package + CLI)
- **Reusable workflow**: `.github/workflows/poc4_7_ci.yml`
- **Report-only fixture test**: `.github/workflows/poc4_7_report_fixture_test.yml`
- **Roadmap**: `ROADMAP.md` (RFP-aligned priorities)
- **Docs**: `docs/` (implementation spec, pipeline brainstorming, RFP copy)

## Quick start (use from another repo)

Add the reusable workflow to your repo (example). This runs the PoC pipeline in this repo, while cloning the specs and client at runtime.

```yaml
name: Run eth-llm PoC

on:
  workflow_dispatch:

jobs:
  run-poc:
    uses: petroslamb/eth-llm-poc/.github/workflows/poc4_7_ci.yml@main
    with:
      eip: "7702"
      fork: "prague"
      client: "geth"
      model: "claude-sonnet-4-5"
      phases: "phase2B"
      max_turns: "20"
      eips_ref: "master"
      execution_specs_ref: "mainnet"
      client_ref: ""
    secrets:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Inputs (reusable workflow)

- **eip**: EIP number (e.g., `7702`)
- **fork**: Execution-specs fork name (e.g., `prague`)
- **client**: Execution client (default `geth`)
- **model**: `claude-haiku-4-5`, `claude-sonnet-4-5`, `claude-opus-4-5`
- **phases**: Comma-separated list. Later phases auto-include prerequisites. Example: `phase1A,phase1B,phase2B`
- **max_turns**: Agent run count (default `20`)
- **eips_ref / execution_specs_ref**: Git refs used for shallow checkout
- **client_ref**: Optional client ref override (branch/tag/commit). If empty, uses the default ref for the selected client.

## Report-only fixture test

Run the fixture-based report job without invoking the full pipeline. This is useful for validating report rendering and summaries.

```yaml
jobs:
  report-fixture:
    uses: petroslamb/eth-llm-poc/.github/workflows/poc4_7_report_fixture_test.yml@main
```

## Artifacts

The workflow uploads the full run directory (including CSVs, prompts, outputs, and summaries) so you can inspect everything as if it were a local run.

## Notes

- This repo contains **no** execution-specs, EIPs, or execution client submodules. Those are fetched shallowly by the workflow at runtime.
- Defaults are aligned with the current PoC 4.7/4.8 configuration in `eth-llm`.
