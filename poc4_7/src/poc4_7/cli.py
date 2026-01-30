"""CLI for PoC 4.7 phases."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .config import load_config
from .reporting import write_report
from .agents import AgentProtocol, ClaudeAgent
from .runner import run_phase_0a, run_phase_1a, run_phase_1b, run_phase_2a, run_phase_2b
from .spec_index import run_index_specs
from .utils import timestamp


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PoC 4.7 phase runner")
    parser.add_argument(
        "--phase",
        required=True,
        choices=["0A", "1A", "1B", "2A", "2B"],
        help="Phase to run: 0A, 1A, 1B, 2A, or 2B",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to config.yaml (optional, looks for config.yaml in cwd if not specified).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for outputs (defaults to ./poc4_7_runs/<timestamp>).",
    )
    parser.add_argument(
        "--eip-file",
        default=None,
        help="Path to an EIP markdown file (required for phase 0A).",
    )
    parser.add_argument(
        "--eip",
        default=None,
        help="EIP number or eip-<num> (inferred from --eip-file if not provided).",
    )
    parser.add_argument(
        "--fork",
        default=None,
        help="Execution-specs fork name (default: london).",
    )
    parser.add_argument(
        "--spec-repo",
        default=None,
        help="Path to execution-specs repo root (required for phases 0A, 1A).",
    )
    parser.add_argument(
        "--parent-run",
        default=None,
        help="Path to previous phase run folder (required for phases 1A, 1B, 2A, 2B).",
    )
    parser.add_argument(
        "--obligation-id",
        default=None,
        help="Limit processing to a single obligation ID (phases 1A/1B/2A/2B).",
    )
    parser.add_argument(
        "--client-repo",
        default=None,
        help="Path to the execution client repo root (required for phases 2A, 2B).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Claude model identifier (optional).",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=None,
        help="Maximum turns per Claude query (defaults to config or 1).",
    )
    parser.add_argument(
        "--allowed-tools",
        default=None,
        help="Comma-separated list of allowed tools (default: Read,Write,Bash,Grep,Glob).",
    )
    parser.add_argument(
        "--llm-mode",
        default=None,
        choices=["live", "fake"],
        help="LLM mode: live (default) or fake (record-only).",
    )
    parser.add_argument(
        "--record-llm-calls",
        action="store_true",
        help="Record LLM call metadata alongside outputs.",
    )
    return parser


def build_index_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PoC 4.7 spec indexer")
    parser.add_argument(
        "--spec-repo",
        required=True,
        help="Path to execution-specs repo root (required).",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory for index outputs (required).",
    )
    parser.add_argument(
        "--spec-readme",
        default=None,
        help="Path to execution-specs README.md (default: <spec-repo>/README.md).",
    )
    parser.add_argument(
        "--eip-fork-map",
        default=None,
        help="Path to write eip_fork_map.json (default: <output-dir>/eip_fork_map.json).",
    )
    parser.add_argument(
        "--spec-index",
        default=None,
        help="Path to write spec_index.json (default: <output-dir>/spec_index.json).",
    )
    parser.add_argument(
        "--run-manifest",
        default=None,
        help="Path to write run_manifest.json (default: <output-dir>/run_manifest.json).",
    )
    return parser


def build_report_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PoC 4.7 run report generator")
    parser.add_argument(
        "--run-root",
        default=None,
        help="Run root or any nested run path (defaults to current working directory).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for summary outputs (defaults to run root).",
    )
    parser.add_argument(
        "--formats",
        default="json,md",
        help="Comma-separated formats to emit (json,md).",
    )
    return parser


def resolve_agent(llm_mode: str) -> AgentProtocol:
    if llm_mode == "fake":
        from .fake_agent import FakeClaudeAgent

        return FakeClaudeAgent()
    return ClaudeAgent()


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "index-specs":
        index_parser = build_index_parser()
        index_args = index_parser.parse_args(sys.argv[2:])
        run_index_specs(
            spec_repo=index_args.spec_repo,
            output_dir=index_args.output_dir,
            spec_readme=index_args.spec_readme,
            eip_fork_map_path=index_args.eip_fork_map,
            spec_index_path=index_args.spec_index,
            run_manifest_path=index_args.run_manifest,
        )
        return 0
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        report_parser = build_report_parser()
        report_args = report_parser.parse_args(sys.argv[2:])
        run_root = (
            Path(report_args.run_root).resolve()
            if report_args.run_root
            else Path.cwd().resolve()
        )
        formats = [f.strip() for f in report_args.formats.split(",") if f.strip()]
        write_report(
            run_root=run_root,
            output_dir=report_args.output_dir,
            formats=formats,
        )
        return 0

    parser = build_parser()
    args = parser.parse_args()

    # Load config from explicit path, cwd, or skip if not found
    cfg: dict = {}
    if args.config:
        config_path = Path(args.config).resolve()
        cfg = load_config(config_path)
    else:
        cwd_config = Path.cwd() / "config.yaml"
        if cwd_config.exists():
            cfg = load_config(cwd_config)

    # Resolve output directory
    output_dir = args.output_dir or cfg.get("output_dir")
    if not output_dir:
        output_dir = str(Path.cwd() / "poc4_7_runs" / timestamp())

    eip_file = args.eip_file or cfg.get("eip_file")
    eip_number = args.eip or cfg.get("eip") or cfg.get("eip_number")
    fork = args.fork or cfg.get("fork")
    spec_repo = args.spec_repo or cfg.get("spec_repo")
    model = args.model or cfg.get("model")
    max_turns = args.max_turns if args.max_turns is not None else cfg.get("max_turns", 1)
    client_repo = args.client_repo or cfg.get("client_repo")
    allowed_tools = cfg.get("allowed_tools")
    if args.allowed_tools:
        allowed_tools = [t.strip() for t in args.allowed_tools.split(",") if t.strip()]

    llm_mode = args.llm_mode or cfg.get("llm_mode") or os.getenv("POC4_7_LLM_MODE", "")
    llm_mode = (llm_mode or "live").strip().lower()
    if llm_mode not in {"live", "fake"}:
        parser.error("--llm-mode must be 'live' or 'fake'")

    record_llm_calls = bool(cfg.get("record_llm_calls", False))
    env_record = os.getenv("POC4_7_RECORD_LLM_CALLS", "").strip().lower()
    if env_record in {"1", "true", "yes", "y"}:
        record_llm_calls = True
    if args.record_llm_calls:
        record_llm_calls = True

    agent = resolve_agent(llm_mode)

    if args.phase == "0A":
        if not eip_file:
            parser.error("--eip-file is required for phase 0A")
        if not spec_repo:
            parser.error("--spec-repo is required for phase 0A")
        run_phase_0a(
            eip_file=eip_file,
            spec_repo=spec_repo,
            output_dir=output_dir,
            eip_number=eip_number,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            llm_mode=llm_mode,
            record_llm_calls=record_llm_calls,
            agent=agent,
        )
        return 0

    if args.phase == "1A":
        if not args.parent_run:
            parser.error("--parent-run is required for phase 1A")
        if not spec_repo:
            parser.error("--spec-repo is required for phase 1A")
        run_phase_1a(
            parent_run=Path(args.parent_run).resolve(),
            spec_repo=spec_repo,
            eip_number=eip_number,
            fork=fork,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            llm_mode=llm_mode,
            record_llm_calls=record_llm_calls,
            obligation_id=args.obligation_id,
            agent=agent,
        )
        return 0

    if args.phase == "1B":
        if not args.parent_run:
            parser.error("--parent-run is required for phase 1B")
        run_phase_1b(
            parent_run=Path(args.parent_run).resolve(),
            spec_repo=spec_repo,  # Can be None, will be inferred from parent manifest
            eip_number=eip_number,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            llm_mode=llm_mode,
            record_llm_calls=record_llm_calls,
            obligation_id=args.obligation_id,
            agent=agent,
        )
        return 0

    if args.phase == "2A":
        if not args.parent_run:
            parser.error("--parent-run is required for phase 2A")
        if not client_repo:
            parser.error("--client-repo is required for phase 2A")
        run_phase_2a(
            parent_run=Path(args.parent_run).resolve(),
            client_repo=client_repo,
            eip_number=eip_number,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            llm_mode=llm_mode,
            record_llm_calls=record_llm_calls,
            obligation_id=args.obligation_id,
            agent=agent,
        )
        return 0

    if args.phase == "2B":
        if not args.parent_run:
            parser.error("--parent-run is required for phase 2B")
        if not client_repo:
            parser.error("--client-repo is required for phase 2B")
        run_phase_2b(
            parent_run=Path(args.parent_run).resolve(),
            client_repo=client_repo,
            eip_number=eip_number,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            llm_mode=llm_mode,
            record_llm_calls=record_llm_calls,
            obligation_id=args.obligation_id,
            agent=agent,
        )
        return 0

    parser.error("Unknown phase")
    return 1
