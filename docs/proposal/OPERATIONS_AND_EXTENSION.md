# Operations and Extension

This document covers setup, maintenance, and extension guidance for PoC 5. For detailed CLI usage, see `poc5/README.md` and `poc5/docs/POC_IMPLEMENTATION_SPEC.md`.

## Setup (Local)

| Step | Command / Location | Notes |
| --- | --- | --- |
| Install | `pip install -e .` | From `poc5/` |
| Configure | `example_config.yaml` | Copy to `config.yaml` if desired |
| Credentials | `ANTHROPIC_API_KEY` | Required for `--llm-mode live` |

## Maintenance Tasks

| Task | Cadence | Notes |
| --- | --- | --- |
| Update spec refs | As forks update | Use workflow inputs or local repo refs |
| Refresh client refs | As client releases | Update `client_ref` in workflows |
| Review prompts | As scope changes | `poc5/src/eip_verify/prompts/` |
| Manage artifacts | Per run | Archive `runs/` outputs for audit |
| Validate outputs | Per run | Check `summary.md` and CSVs |

## Extension Points

| Goal | Touchpoints | Notes |
| --- | --- | --- |
| Add a new client | Workflow refs and `client` list | Extend repo mapping in `ci.yml` if needed |
| Add new phase | `runner.py`, `pipeline.py`, prompts | Also update reporting expectations |
| Add new output format | `reporting.py` | SARIF is a planned extension |
| Expand to consensus-specs | New indexer + prompts | Coordinate with `CONSENSUS_SPECS_OVERVIEW.md` |
| Improve triage logic | CSV schema + reporting | Consider adding scoring metadata |
