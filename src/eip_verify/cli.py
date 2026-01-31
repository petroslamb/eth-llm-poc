"""CLI for EIP verification using Fire."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import fire

from .agents import ClaudeAgent
from .config import load_config
from .pipeline import run_pipeline
from .reporting import write_report
from .runner import run_phase_0a, run_phase_1a, run_phase_1b, run_phase_2a, run_phase_2b
from .spec_index import run_index_specs
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
        """Extract obligations from EIP markdown."""
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
        """Find implementation locations in execution-specs."""
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
        """Analyze code flow and gaps in spec."""
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
        """Find implementation locations in client repo."""
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
        """Analyze code flow and gaps in client."""
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
        """Run multiple verification phases in sequence."""
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


def main():
    fire.Fire(CLI)
