"""CLI for EIP verification using Fire."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Optional

import fire

from .agents import ClaudeAgent
from .config import load_config
from .pipeline import run_pipeline
from .reporting import write_report
from .runner import run_phase_0a, run_phase_1a, run_phase_1b, run_phase_2a, run_phase_2b
from .spec_index import run_index_specs
from . import spec_index
from .utils import timestamp


def _resolve_config(config: Optional[str] = None) -> dict:
    """Load config from explicit path, cwd, or return empty."""
    if config:
        return load_config(Path(config).resolve())
    cwd_config = Path.cwd() / "config.yaml"
    if cwd_config.exists():
        return load_config(cwd_config)
    return {}


def _resolve_agent(llm_mode: str):
    """Get the appropriate agent based on mode."""
    if llm_mode == "fake":
        from .fake_agent import FakeClaudeAgent
        return FakeClaudeAgent()
    return ClaudeAgent()


def _resolve_llm_mode(llm_mode: Optional[str], cfg: dict) -> str:
    """Resolve LLM mode from arg, config, or env."""
    mode = llm_mode or cfg.get("llm_mode") or os.getenv("EIP_VERIFY_LLM_MODE", "live")
    return mode.strip().lower()


def _resolve_record_calls(record_llm_calls: bool, cfg: dict) -> bool:
    """Resolve record_llm_calls from arg, config, or env."""
    if record_llm_calls:
        return True
    if cfg.get("record_llm_calls"):
        return True
    env_val = os.getenv("EIP_VERIFY_RECORD_LLM_CALLS", "").strip().lower()
    return env_val in {"1", "true", "yes", "y"}


class CLI:
    """LLM-powered verification of EIP obligations against execution-specs and client implementations."""

    def extract(
        self,
        eip_file: str,
        spec_repo: str,
        eip: Optional[str] = None,
        output_dir: Optional[str] = None,
        config: Optional[str] = None,
        model: Optional[str] = None,
        max_turns: Optional[int] = None,
        allowed_tools: Optional[str] = None,
        llm_mode: Optional[str] = None,
        record_llm_calls: bool = False,
    ):
        """
        Extract obligations from EIP markdown.

        Args:
            eip_file: Path to the EIP markdown file.
            spec_repo: Path to the execution-specs repository.
            eip: EIP number (e.g., "1559").
            output_dir: Directory to save results.
            config: Path to a YAML config file (default: config.yaml in CWD).
            model: LLM model to use.
            max_turns: Maximum conversation turns.
            allowed_tools: Comma-separated list of allowed tools.
            llm_mode: Agent mode ("live" or "fake").
            record_llm_calls: Whether to record LLM interactions.
        """
        cfg = _resolve_config(config)
        llm_mode = _resolve_llm_mode(llm_mode, cfg)
        run_phase_0a(
            eip_file=eip_file or cfg.get("eip_file"),
            spec_repo=spec_repo or cfg.get("spec_repo"),
            output_dir=output_dir or cfg.get("output_dir") or str(Path.cwd() / "runs" / timestamp()),
            eip_number=eip or cfg.get("eip") or cfg.get("eip_number"),
            model=model or cfg.get("model"),
            max_turns=max_turns if max_turns is not None else cfg.get("max_turns", 1),
            allowed_tools=allowed_tools.split(",") if allowed_tools else cfg.get("allowed_tools"),
            llm_mode=llm_mode,
            record_llm_calls=_resolve_record_calls(record_llm_calls, cfg),
            agent=_resolve_agent(llm_mode),
        )

    def locate_spec(
        self,
        parent_run: str,
        spec_repo: str,
        eip: Optional[str] = None,
        fork: Optional[str] = None,
        config: Optional[str] = None,
        model: Optional[str] = None,
        max_turns: Optional[int] = None,
        allowed_tools: Optional[str] = None,
        llm_mode: Optional[str] = None,
        record_llm_calls: bool = False,
        obligation_id: Optional[str] = None,
    ):
        """
        Find implementation locations in execution-specs.

        Args:
            parent_run: Path to the output directory of the previous 'extract' phase.
            spec_repo: Path to the execution-specs repository.
            eip: EIP number.
            fork: Target fork name (e.g., "london").
            config: Path to a YAML config file.
            model: LLM model to use.
            max_turns: Maximum conversation turns.
            allowed_tools: Comma-separated list of tools.
            llm_mode: Agent mode ("live" or "fake").
            record_llm_calls: Whether to record LLM interactions.
            obligation_id: Specific obligation ID to locate.
        """
        cfg = _resolve_config(config)
        llm_mode = _resolve_llm_mode(llm_mode, cfg)
        run_phase_1a(
            parent_run=Path(parent_run).resolve(),
            spec_repo=spec_repo or cfg.get("spec_repo"),
            eip_number=eip or cfg.get("eip") or cfg.get("eip_number"),
            fork=fork or cfg.get("fork"),
            model=model or cfg.get("model"),
            max_turns=max_turns if max_turns is not None else cfg.get("max_turns", 1),
            allowed_tools=allowed_tools.split(",") if allowed_tools else cfg.get("allowed_tools"),
            llm_mode=llm_mode,
            record_llm_calls=_resolve_record_calls(record_llm_calls, cfg),
            obligation_id=obligation_id,
            agent=_resolve_agent(llm_mode),
        )

    def analyze_spec(
        self,
        parent_run: str,
        eip: Optional[str] = None,
        spec_repo: Optional[str] = None,
        config: Optional[str] = None,
        model: Optional[str] = None,
        max_turns: Optional[int] = None,
        allowed_tools: Optional[str] = None,
        llm_mode: Optional[str] = None,
        record_llm_calls: bool = False,
        obligation_id: Optional[str] = None,
    ):
        """
        Analyze code flow and gaps in spec.

        Args:
            parent_run: Path to the output directory of the previous 'locate-spec' phase.
            eip: EIP number.
            spec_repo: Path to the execution-specs repository.
            config: Path to a YAML config file.
            model: LLM model to use.
            max_turns: Maximum conversation turns.
            allowed_tools: Comma-separated list of tools.
            llm_mode: Agent mode ("live" or "fake").
            record_llm_calls: Whether to record LLM interactions.
            obligation_id: Specific obligation ID to analyze.
        """
        cfg = _resolve_config(config)
        llm_mode = _resolve_llm_mode(llm_mode, cfg)
        run_phase_1b(
            parent_run=Path(parent_run).resolve(),
            spec_repo=spec_repo or cfg.get("spec_repo"),
            eip_number=eip or cfg.get("eip") or cfg.get("eip_number"),
            model=model or cfg.get("model"),
            max_turns=max_turns if max_turns is not None else cfg.get("max_turns", 1),
            allowed_tools=allowed_tools.split(",") if allowed_tools else cfg.get("allowed_tools"),
            llm_mode=llm_mode,
            record_llm_calls=_resolve_record_calls(record_llm_calls, cfg),
            obligation_id=obligation_id,
            agent=_resolve_agent(llm_mode),
        )

    def locate_client(
        self,
        parent_run: str,
        client_repo: str,
        eip: Optional[str] = None,
        config: Optional[str] = None,
        model: Optional[str] = None,
        max_turns: Optional[int] = None,
        allowed_tools: Optional[str] = None,
        llm_mode: Optional[str] = None,
        record_llm_calls: bool = False,
        obligation_id: Optional[str] = None,
    ):
        """
        Find implementation locations in client repo.

        Args:
            parent_run: Path to the output directory of the previous phase.
            client_repo: Path to the client repository (e.g., go-ethereum).
            eip: EIP number.
            config: Path to a YAML config file.
            model: LLM model to use.
            max_turns: Maximum conversation turns.
            allowed_tools: Comma-separated list of tools.
            llm_mode: Agent mode ("live" or "fake").
            record_llm_calls: Whether to record LLM interactions.
            obligation_id: Specific obligation ID to locate.
        """
        cfg = _resolve_config(config)
        llm_mode = _resolve_llm_mode(llm_mode, cfg)
        run_phase_2a(
            parent_run=Path(parent_run).resolve(),
            client_repo=client_repo or cfg.get("client_repo"),
            eip_number=eip or cfg.get("eip") or cfg.get("eip_number"),
            model=model or cfg.get("model"),
            max_turns=max_turns if max_turns is not None else cfg.get("max_turns", 1),
            allowed_tools=allowed_tools.split(",") if allowed_tools else cfg.get("allowed_tools"),
            llm_mode=llm_mode,
            record_llm_calls=_resolve_record_calls(record_llm_calls, cfg),
            obligation_id=obligation_id,
            agent=_resolve_agent(llm_mode),
        )

    def analyze_client(
        self,
        parent_run: str,
        client_repo: str,
        eip: Optional[str] = None,
        config: Optional[str] = None,
        model: Optional[str] = None,
        max_turns: Optional[int] = None,
        allowed_tools: Optional[str] = None,
        llm_mode: Optional[str] = None,
        record_llm_calls: bool = False,
        obligation_id: Optional[str] = None,
    ):
        """
        Analyze code flow and gaps in client.

        Args:
            parent_run: Path to the output directory of the previous phase.
            client_repo: Path to the client repository.
            eip: EIP number.
            config: Path to a YAML config file.
            model: LLM model to use.
            max_turns: Maximum conversation turns.
            allowed_tools: Comma-separated list of tools.
            llm_mode: Agent mode ("live" or "fake").
            record_llm_calls: Whether to record LLM interactions.
            obligation_id: Specific obligation ID to analyze.
        """
        cfg = _resolve_config(config)
        llm_mode = _resolve_llm_mode(llm_mode, cfg)
        run_phase_2b(
            parent_run=Path(parent_run).resolve(),
            client_repo=client_repo or cfg.get("client_repo"),
            eip_number=eip or cfg.get("eip") or cfg.get("eip_number"),
            model=model or cfg.get("model"),
            max_turns=max_turns if max_turns is not None else cfg.get("max_turns", 1),
            allowed_tools=allowed_tools.split(",") if allowed_tools else cfg.get("allowed_tools"),
            llm_mode=llm_mode,
            record_llm_calls=_resolve_record_calls(record_llm_calls, cfg),
            obligation_id=obligation_id,
            agent=_resolve_agent(llm_mode),
        )

    def pipeline(
        self,
        eip: str,
        phases: str,
        spec_repo: str,
        client_repo: Optional[str] = None,
        eip_file: Optional[str] = None,
        fork: Optional[str] = None,
        output_dir: Optional[str] = None,
        config: Optional[str] = None,
        model: Optional[str] = None,
        max_turns: Optional[int] = None,
        allowed_tools: Optional[str] = None,
        llm_mode: Optional[str] = None,
        record_llm_calls: bool = False,
        obligation_id: Optional[str] = None,
    ):
        """
        Run multiple verification phases in sequence.

        Args:
            eip: EIP number (e.g., "1559").
            phases: Comma-separated list of phases to run.
            spec_repo: Path to the execution-specs repository.
            client_repo: Path to the client repository.
            eip_file: Path to specific EIP markdown file (optional).
            fork: Target fork name.
            output_dir: Directory to save results.
            config: Path to a YAML config file.
            model: LLM model to use.
            max_turns: Maximum turns per phase.
            allowed_tools: Comma-separated list of tools.
            llm_mode: Agent mode ("live" or "fake").
            record_llm_calls: Whether to record LLM interactions.
            obligation_id: Specific obligation ID to verify.
        """
        cfg = _resolve_config(config)
        llm_mode = _resolve_llm_mode(llm_mode, cfg)
        run_pipeline(
            eip=str(eip),
            phases=phases.split(","),
            spec_repo=spec_repo or cfg.get("spec_repo"),
            client_repo=client_repo or cfg.get("client_repo"),
            eip_file=eip_file or cfg.get("eip_file"),
            fork=fork or cfg.get("fork"),
            output_dir=output_dir or cfg.get("output_dir"),
            model=model or cfg.get("model"),
            max_turns=max_turns if max_turns is not None else cfg.get("max_turns", 20),
            allowed_tools=allowed_tools.split(",") if allowed_tools else cfg.get("allowed_tools"),
            llm_mode=llm_mode,
            record_llm_calls=_resolve_record_calls(record_llm_calls, cfg),
            obligation_id=obligation_id,
            agent=_resolve_agent(llm_mode),
        )

    def index_specs(
        self,
        spec_repo: str,
        output_dir: str,
        spec_readme: Optional[str] = None,
        eip_fork_map: Optional[str] = None,
        spec_index: Optional[str] = None,
        run_manifest: Optional[str] = None,
    ):
        """Generate spec index and EIP→fork mapping."""
        run_index_specs(
            spec_repo=spec_repo,
            output_dir=output_dir,
            spec_readme=spec_readme,
            eip_fork_map_path=eip_fork_map,
            spec_index_path=spec_index,
            run_manifest_path=run_manifest,
        )

    def report(
        self,
        run_root: Optional[str] = None,
        output_dir: Optional[str] = None,
        formats: str = "json,md",
    ):
        """Generate run summary report."""
        root = Path(run_root).resolve() if run_root else Path.cwd().resolve()
        fmt_list = [f.strip() for f in formats.split(",") if f.strip()]
        write_report(run_root=root, output_dir=output_dir, formats=fmt_list)


    def get_matrix(
        self,
        spec_repo: str,
        fork: str,
        eip: Optional[str] = None,
    ):
        """
        Resolve EIP matrix for CI.

        Args:
            spec_repo: Path to execution-specs repo.
            fork: Fork name (e.g. London).
            eip: Optional comma-separated list of EIPs.
        """
        resolved_spec_repo = Path(spec_repo).resolve()
        
        # Determine strict eip list
        eip_list = []
        if eip is not None:
            if isinstance(eip, (list, tuple)):
                # Flatten valid items
                for item in eip:
                    if isinstance(item, str):
                        eip_list.extend([x.strip() for x in item.split(",") if x.strip()])
                    else:
                        eip_list.append(str(item))
            elif isinstance(eip, str):
                eip_list = [e.strip() for e in eip.split(",") if e.strip()]
            else:
                eip_list = [str(eip)]
        
        # 1. If explicit EIPs provided, use them
        if eip_list:
            print(json.dumps(eip_list))
            return

        # 2. If no EIPs, look up the fork in the spec repo
        if not resolved_spec_repo.exists():
            # Print error to stderr so it doesn't pollute the JSON output on stdout (if captured blindly)
            # But normally fire handles exceptions.
            raise FileNotFoundError(f"Spec repo not found at {resolved_spec_repo}")

        readme_path = resolved_spec_repo / "README.md"
        if not readme_path.exists():
            raise FileNotFoundError(f"Spec README not found at {readme_path}")

        # Use the existing logic to parse the table
        eip_fork_map = spec_index.build_eip_fork_map(readme_path, resolved_spec_repo)
        
        forks_data = eip_fork_map.get("forks", [])
        # Case-insensitive lookup
        target_fork_data = next((f for f in forks_data if f["fork"].lower() == fork.lower()), None)

        if not target_fork_data:
            available = [f["fork"] for f in forks_data]
            raise ValueError(f"Fork '{fork}' not found in spec README. Available: {available}")

        # Prefer the 'eips_fork_init' (actual python code) if available, 
        # otherwise fallback to 'eips_readme' (table)
        eips = target_fork_data.get("eips_fork_init")
        if eips is None:
            eips = target_fork_data.get("eips_readme")
        
        # Convert to strings
        result = [str(e) for e in eips] if eips else []
        print(json.dumps(result))


def main():
    fire.Fire(CLI)
