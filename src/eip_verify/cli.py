"""CLI for EIP verification."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .agents import AgentProtocol, ClaudeAgent
from .config import load_config
from .reporting import write_report
from .runner import run_phase_0a, run_phase_1a, run_phase_1b, run_phase_2a, run_phase_2b
from .spec_index import run_index_specs
from .utils import timestamp


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add common arguments shared across subcommands."""
    parser.add_argument(
        "--config",
        default=None,
        help="Path to config.yaml (optional, looks for config.yaml in cwd if not specified).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for outputs (defaults to ./runs/<timestamp>).",
    )
    parser.add_argument(
        "--eip",
        default=None,
        help="EIP number or eip-<num> (inferred from --eip-file if not provided).",
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eip-verify",
        description="LLM-powered verification of EIP obligations against execution-specs and client implementations.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # extract (was phase 0A)
    extract = subparsers.add_parser(
        "extract",
        help="Extract obligations from EIP markdown",
        description="Parse an EIP markdown file and extract verifiable obligations.",
    )
    add_common_args(extract)
    extract.add_argument(
        "--eip-file",
        required=True,
        help="Path to an EIP markdown file.",
    )
    extract.add_argument(
        "--spec-repo",
        required=True,
        help="Path to execution-specs repo root.",
    )

    # locate-spec (was phase 1A)
    locate_spec = subparsers.add_parser(
        "locate-spec",
        help="Find implementation locations in execution-specs",
        description="Locate where each obligation is implemented in the execution-specs.",
    )
    add_common_args(locate_spec)
    locate_spec.add_argument(
        "--parent-run",
        required=True,
        help="Path to previous phase run folder.",
    )
    locate_spec.add_argument(
        "--spec-repo",
        required=True,
        help="Path to execution-specs repo root.",
    )
    locate_spec.add_argument(
        "--fork",
        default=None,
        help="Execution-specs fork name (default: london).",
    )
    locate_spec.add_argument(
        "--obligation-id",
        default=None,
        help="Limit processing to a single obligation ID.",
    )

    # analyze-spec (was phase 1B)
    analyze_spec = subparsers.add_parser(
        "analyze-spec",
        help="Analyze code flow and gaps in spec",
        description="Analyze code flow and identify gaps for each obligation in execution-specs.",
    )
    add_common_args(analyze_spec)
    analyze_spec.add_argument(
        "--parent-run",
        required=True,
        help="Path to previous phase run folder.",
    )
    analyze_spec.add_argument(
        "--spec-repo",
        default=None,
        help="Path to execution-specs repo root (inferred from parent manifest if not provided).",
    )
    analyze_spec.add_argument(
        "--obligation-id",
        default=None,
        help="Limit processing to a single obligation ID.",
    )

    # locate-client (was phase 2A)
    locate_client = subparsers.add_parser(
        "locate-client",
        help="Find implementation locations in client repo",
        description="Locate where each obligation is implemented in that execution client.",
    )
    add_common_args(locate_client)
    locate_client.add_argument(
        "--parent-run",
        required=True,
        help="Path to previous phase run folder.",
    )
    locate_client.add_argument(
        "--client-repo",
        required=True,
        help="Path to the execution client repo root.",
    )
    locate_client.add_argument(
        "--obligation-id",
        default=None,
        help="Limit processing to a single obligation ID.",
    )

    # analyze-client (was phase 2B)
    analyze_client = subparsers.add_parser(
        "analyze-client",
        help="Analyze code flow and gaps in client",
        description="Analyze code flow and identify gaps for each obligation in the client.",
    )
    add_common_args(analyze_client)
    analyze_client.add_argument(
        "--parent-run",
        required=True,
        help="Path to previous phase run folder.",
    )
    analyze_client.add_argument(
        "--client-repo",
        required=True,
        help="Path to the execution client repo root.",
    )
    analyze_client.add_argument(
        "--obligation-id",
        default=None,
        help="Limit processing to a single obligation ID.",
    )

    # index-specs
    index_specs = subparsers.add_parser(
        "index-specs",
        help="Generate spec index and EIP→fork mapping",
        description="Parse execution-specs to generate EIP-to-fork mappings and spec index.",
    )
    index_specs.add_argument(
        "--spec-repo",
        required=True,
        help="Path to execution-specs repo root.",
    )
    index_specs.add_argument(
        "--output-dir",
        required=True,
        help="Directory for index outputs.",
    )
    index_specs.add_argument(
        "--spec-readme",
        default=None,
        help="Path to execution-specs README.md (default: <spec-repo>/README.md).",
    )
    index_specs.add_argument(
        "--eip-fork-map",
        default=None,
        help="Path to write eip_fork_map.json (default: <output-dir>/eip_fork_map.json).",
    )
    index_specs.add_argument(
        "--spec-index",
        default=None,
        help="Path to write spec_index.json (default: <output-dir>/spec_index.json).",
    )
    index_specs.add_argument(
        "--run-manifest",
        default=None,
        help="Path to write run_manifest.json (default: <output-dir>/run_manifest.json).",
    )

    # report
    report = subparsers.add_parser(
        "report",
        help="Generate run summary report",
        description="Generate summary reports (JSON/MD) for a completed run.",
    )
    report.add_argument(
        "--run-root",
        default=None,
        help="Run root or any nested run path (defaults to current working directory).",
    )
    report.add_argument(
        "--output-dir",
        default=None,
        help="Directory for summary outputs (defaults to run root).",
    )
    report.add_argument(
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
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    # Handle index-specs command (no common args)
    if args.command == "index-specs":
        run_index_specs(
            spec_repo=args.spec_repo,
            output_dir=args.output_dir,
            spec_readme=args.spec_readme,
            eip_fork_map_path=args.eip_fork_map,
            spec_index_path=args.spec_index,
            run_manifest_path=args.run_manifest,
        )
        return 0

    # Handle report command
    if args.command == "report":
        run_root = (
            Path(args.run_root).resolve()
            if args.run_root
            else Path.cwd().resolve()
        )
        formats = [f.strip() for f in args.formats.split(",") if f.strip()]
        write_report(
            run_root=run_root,
            output_dir=args.output_dir,
            formats=formats,
        )
        return 0

    # Commands with common args
    cfg: dict = {}
    if hasattr(args, "config") and args.config:
        config_path = Path(args.config).resolve()
        cfg = load_config(config_path)
    else:
        cwd_config = Path.cwd() / "config.yaml"
        if cwd_config.exists():
            cfg = load_config(cwd_config)

    # Resolve output directory
    output_dir = getattr(args, "output_dir", None) or cfg.get("output_dir")
    if not output_dir:
        output_dir = str(Path.cwd() / "runs" / timestamp())

    eip_file = getattr(args, "eip_file", None) or cfg.get("eip_file")
    eip_number = getattr(args, "eip", None) or cfg.get("eip") or cfg.get("eip_number")
    fork = getattr(args, "fork", None) or cfg.get("fork")
    spec_repo = getattr(args, "spec_repo", None) or cfg.get("spec_repo")
    model = getattr(args, "model", None) or cfg.get("model")
    max_turns = args.max_turns if getattr(args, "max_turns", None) is not None else cfg.get("max_turns", 1)
    client_repo = getattr(args, "client_repo", None) or cfg.get("client_repo")
    allowed_tools = cfg.get("allowed_tools")
    if getattr(args, "allowed_tools", None):
        allowed_tools = [t.strip() for t in args.allowed_tools.split(",") if t.strip()]

    llm_mode = getattr(args, "llm_mode", None) or cfg.get("llm_mode") or os.getenv("EIP_VERIFY_LLM_MODE", "")
    llm_mode = (llm_mode or "live").strip().lower()
    if llm_mode not in {"live", "fake"}:
        parser.error("--llm-mode must be 'live' or 'fake'")

    record_llm_calls = bool(cfg.get("record_llm_calls", False))
    env_record = os.getenv("EIP_VERIFY_RECORD_LLM_CALLS", "").strip().lower()
    if env_record in {"1", "true", "yes", "y"}:
        record_llm_calls = True
    if getattr(args, "record_llm_calls", False):
        record_llm_calls = True

    agent = resolve_agent(llm_mode)

    if args.command == "extract":
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

    if args.command == "locate-spec":
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
            obligation_id=getattr(args, "obligation_id", None),
            agent=agent,
        )
        return 0

    if args.command == "analyze-spec":
        run_phase_1b(
            parent_run=Path(args.parent_run).resolve(),
            spec_repo=spec_repo,
            eip_number=eip_number,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            llm_mode=llm_mode,
            record_llm_calls=record_llm_calls,
            obligation_id=getattr(args, "obligation_id", None),
            agent=agent,
        )
        return 0

    if args.command == "locate-client":
        run_phase_2a(
            parent_run=Path(args.parent_run).resolve(),
            client_repo=client_repo,
            eip_number=eip_number,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            llm_mode=llm_mode,
            record_llm_calls=record_llm_calls,
            obligation_id=getattr(args, "obligation_id", None),
            agent=agent,
        )
        return 0

    if args.command == "analyze-client":
        run_phase_2b(
            parent_run=Path(args.parent_run).resolve(),
            client_repo=client_repo,
            eip_number=eip_number,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            llm_mode=llm_mode,
            record_llm_calls=record_llm_calls,
            obligation_id=getattr(args, "obligation_id", None),
            agent=agent,
        )
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 1
