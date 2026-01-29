"""CLI for PoC 4.7 phases."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .config import load_config
from .reporting import write_report
from .runner import run_phase_0a, run_phase_1a, run_phase_1b, run_phase_2a, run_phase_2b
from .spec_index import run_index_specs


def normalize_repo_root(path: Path) -> Path:
    if (path / "poc4_7" / "pyproject.toml").exists():
        return path
    if path.name == "poc4_7" and (path / "pyproject.toml").exists():
        return path.parent
    return path


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
        help="Path to config.yaml (defaults to poc4_7/config.yaml if present).",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repository root path (defaults to current working directory).",
    )
    parser.add_argument(
        "--eip-file",
        default=None,
        help="Path to an EIP markdown file (optional; overrides --eip).",
    )
    parser.add_argument(
        "--eip",
        default=None,
        help="EIP number or eip-<num> (default: 1559).",
    )
    parser.add_argument(
        "--fork",
        default=None,
        help="Execution-specs fork name (default: london).",
    )
    parser.add_argument(
        "--spec-root",
        default=None,
        help="Path to execution-specs fork root (overrides --fork).",
    )
    parser.add_argument(
        "--parent-run",
        default=None,
        help="Path to previous phase run folder (required for phases 1A and 1B).",
    )
    parser.add_argument(
        "--obligation-id",
        default=None,
        help="Limit processing to a single obligation ID (phases 1A/1B/2A/2B).",
    )
    parser.add_argument(
        "--geth-root",
        default=None,
        help="Path to the geth repo root (legacy alias for --client-root).",
    )
    parser.add_argument(
        "--client",
        default=None,
        help="Client name under clients/execution (default: geth).",
    )
    parser.add_argument(
        "--client-root",
        default=None,
        help="Path to the client repo root (overrides --client).",
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
        "--spec-map-strict",
        action="store_true",
        help="Fail if README vs fork __init__.py EIP lists mismatch for the selected fork.",
    )
    return parser


def build_index_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PoC 4.7 spec indexer")
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repository root path (defaults to current working directory).",
    )
    parser.add_argument(
        "--spec-root",
        default=None,
        help="Path to execution-specs repo root (default: specs/execution-specs).",
    )
    parser.add_argument(
        "--spec-readme",
        default=None,
        help="Path to execution-specs README.md (default: <spec-root>/README.md).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for index outputs (default: poc4_7/notes/generated/index_runs/<timestamp>).",
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


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "index-specs":
        index_parser = build_index_parser()
        index_args = index_parser.parse_args(sys.argv[2:])
        repo_root = (
            Path(index_args.repo_root).resolve()
            if index_args.repo_root
            else Path.cwd().resolve()
        )
        repo_root = normalize_repo_root(repo_root)
        run_index_specs(
            repo_root=repo_root,
            spec_root=index_args.spec_root,
            spec_readme=index_args.spec_readme,
            output_dir=index_args.output_dir,
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

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path.cwd().resolve()
    repo_root = normalize_repo_root(repo_root)
    config_path = Path(args.config).resolve() if args.config else repo_root / "poc4_7" / "config.yaml"
    cfg = load_config(config_path)

    eip_file = args.eip_file or cfg.get("eip_file")
    eip_number = args.eip or cfg.get("eip") or cfg.get("eip_number")
    fork = args.fork or cfg.get("fork")
    spec_root = args.spec_root or cfg.get("spec_root")
    model = args.model or cfg.get("model")
    max_turns = args.max_turns if args.max_turns is not None else cfg.get("max_turns", 1)
    client_name = args.client or cfg.get("client") or cfg.get("client_name")
    client_root = args.client_root or cfg.get("client_root")
    geth_root = args.geth_root or cfg.get("geth_root")
    if not client_root and geth_root:
        client_root = geth_root
    allowed_tools = cfg.get("allowed_tools")
    if args.allowed_tools:
        allowed_tools = [t.strip() for t in args.allowed_tools.split(",") if t.strip()]
    spec_map_strict = bool(cfg.get("spec_map_strict", False))
    env_strict = os.getenv("POC4_7_SPEC_MAP_STRICT", "").strip().lower()
    if env_strict in {"1", "true", "yes", "y"}:
        spec_map_strict = True
    if args.spec_map_strict:
        spec_map_strict = True

    if args.phase == "0A":
        run_phase_0a(
            repo_root=repo_root,
            eip_file=eip_file,
            eip_number=eip_number,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
        )
        return 0

    if args.phase == "1A":
        if not args.parent_run:
            parser.error("--parent-run is required for phase 1A")
        run_phase_1a(
            repo_root=repo_root,
            parent_run=Path(args.parent_run).resolve(),
            eip_number=eip_number,
            fork=fork,
            spec_root=spec_root,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            obligation_id=args.obligation_id,
            spec_map_strict=spec_map_strict,
        )
        return 0

    if args.phase == "1B":
        if not args.parent_run:
            parser.error("--parent-run is required for phase 1B")
        run_phase_1b(
            repo_root=repo_root,
            parent_run=Path(args.parent_run).resolve(),
            eip_number=eip_number,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            obligation_id=args.obligation_id,
        )
        return 0

    if args.phase == "2A":
        if not args.parent_run:
            parser.error("--parent-run is required for phase 2A")
        run_phase_2a(
            repo_root=repo_root,
            parent_run=Path(args.parent_run).resolve(),
            eip_number=eip_number,
            client_name=client_name,
            client_root=client_root,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            obligation_id=args.obligation_id,
        )
        return 0

    if args.phase == "2B":
        if not args.parent_run:
            parser.error("--parent-run is required for phase 2B")
        run_phase_2b(
            repo_root=repo_root,
            parent_run=Path(args.parent_run).resolve(),
            eip_number=eip_number,
            client_name=client_name,
            client_root=client_root,
            model=model,
            max_turns=max_turns,
            allowed_tools=allowed_tools,
            obligation_id=args.obligation_id,
        )
        return 0

    parser.error("Unknown phase")
    return 1
