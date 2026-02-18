# Repository Guidelines

## Project Structure & Module Organization
- `src/eip_verify/` holds the Python package and CLI. Key modules: `cli.py` (entrypoint), `pipeline.py` (phase orchestration), `runner.py` (phase execution), `spec_index.py` (spec indexing), and `reporting.py` (summaries).
- `src/eip_verify/prompts/` contains phase prompt templates (e.g., `phase0A_obligations.txt`). Keep new prompts in this folder and follow the phase naming pattern.
- `tests/` contains pytest tests; add new tests alongside the behavior they cover.
- `docs/` and `examples/` include implementation notes and sample materials.
- `scripts/` holds repo utilities like `sync_workflow_defaults.py`.
- `runs/` and `spec_index_output/` are generated outputs and are gitignored.

## Build, Test, and Development Commands
- `pip install -e .` installs the CLI locally from source.
- `uv venv .venv && source .venv/bin/activate && uv pip install -e .` is an alternative setup using uv.
- `eip-verify pipeline --eip 1559 --spec-repo ~/specs/execution-specs --client-repo ~/clients/geth --model claude-sonnet-4-5` runs a full pipeline.
- `eip-verify index-specs --spec-repo /path/to/execution-specs --output-dir ./index-output` generates a spec index.
- `pip install -e ".[test]" && pytest -q` installs test deps and runs the suite.

## Coding Style & Naming Conventions
- Python >= 3.11; use 4-space indentation and follow standard PEP 8 formatting.
- Use `snake_case` for functions/modules, `PascalCase` for classes, and keep CLI subcommands kebab-case (e.g., `locate-spec`).
- Prompt files should remain text-based and follow the existing phase prefix scheme.

## Testing Guidelines
- Pytest is the test runner; tests live in `tests/` and follow `test_*.py` naming.
- When adding pipeline behavior, include tests that run in `--llm-mode fake` where possible to avoid external calls.

## Commit & Pull Request Guidelines
- Use short, imperative commit subjects; history often uses scope prefixes like `docs:`, `proposal:`, or `refactor:`.
- PRs should include: a concise summary, rationale, tests run (or “not run” with reason), and links to related issues. Share run artifacts via CI outputs rather than committing `runs/`.

## Security & Configuration Tips
- Live runs require `ANTHROPIC_API_KEY`. Keep secrets in environment variables or CI secrets.
- Config precedence is: CLI args → config file (`config.yaml`) → environment variables → defaults. Use `example_config.yaml` as a template.
