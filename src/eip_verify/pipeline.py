"""Pipeline orchestration for multi-phase verification."""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

from .agents import AgentProtocol, ClaudeAgent
from .reporting import write_report
from .runner import run_phase_0a, run_phase_1a, run_phase_1b, run_phase_2a, run_phase_2b
from .utils import timestamp


PHASE_ORDER = ["extract", "locate-spec", "analyze-spec", "locate-client", "analyze-client"]


def run_pipeline(
    eip: str,
    phases: List[str],
    spec_repo: str,
    client_repo: Optional[str] = None,
    eip_file: Optional[str] = None,
    fork: Optional[str] = None,
    output_dir: Optional[str] = None,
    model: Optional[str] = None,
    max_turns: int = 1,
    allowed_tools: Optional[List[str]] = None,
    llm_mode: str = "live",
    record_llm_calls: bool = False,
    obligation_id: Optional[str] = None,
    agent: Optional[AgentProtocol] = None,
):
    """Run multiple verification phases in sequence."""
    
    # Setup run directory
    run_root = Path(output_dir) if output_dir else Path.cwd() / "runs" / timestamp()
    run_root.mkdir(parents=True, exist_ok=True)
    print(f"Pipeline started. Run root: {run_root}")

    # Resolve agent
    if not agent:
        if llm_mode == "fake":
            from .fake_agent import FakeClaudeAgent
            agent = FakeClaudeAgent()
        else:
            agent = ClaudeAgent()

    # Track output paths for chaining
    current_parent_run: Optional[Path] = None
    
    # Validate eip_file for extract phase if needed
    if "extract" in phases:
        if not eip_file:
            # Try to find it in spec_repo if structured
            possible_path = Path(spec_repo) / "EIPs" / f"eip-{eip}.md"
            if possible_path.exists():
                eip_file = str(possible_path)
            else:
                raise ValueError("Phase 'extract' requires --eip-file or a findable EIP in spec-repo")
    
    for phase in PHASE_ORDER:
        if phase not in phases:
            continue
            
        print(f"\n=== Running Phase: {phase} ===")
        
        if phase == "extract":
            run_phase_0a(
                eip_file=eip_file,
                spec_repo=spec_repo,
                output_dir=str(run_root),
                eip_number=eip,
                model=model,
                max_turns=max_turns,
                allowed_tools=allowed_tools,
                llm_mode=llm_mode,
                record_llm_calls=record_llm_calls,
                agent=agent,
            )
            # Find the output folder (it's created inside run_root/phase0A_runs/<timestamp>)
            # This is a bit hacky because runner creates nested timestamps. 
            # In a full refactor, runner should accept exact output path.
            # tailored for now:
            phase_runs = list((run_root / "phase0A_runs").glob("*"))
            if phase_runs:
                current_parent_run = sorted(phase_runs)[-1]
            else:
                raise RuntimeError("Phase extract failed to produce output directory")

        elif phase == "locate-spec":
            if not current_parent_run:
                raise ValueError(f"Cannot run {phase} without previous phase output")
            run_phase_1a(
                parent_run=current_parent_run,
                spec_repo=spec_repo,
                eip_number=eip,
                fork=fork or "london",
                model=model,
                max_turns=max_turns,
                allowed_tools=allowed_tools,
                llm_mode=llm_mode,
                record_llm_calls=record_llm_calls,
                obligation_id=obligation_id,
                agent=agent,
            )
            # Find next parent
            phase_runs = list((current_parent_run / "phase1A_runs").glob("*"))
            if phase_runs:
                current_parent_run = sorted(phase_runs)[-1]

        elif phase == "analyze-spec":
            if not current_parent_run:
                raise ValueError(f"Cannot run {phase} without previous phase output")
            run_phase_1b(
                parent_run=current_parent_run,
                spec_repo=spec_repo,
                eip_number=eip,
                model=model,
                max_turns=max_turns,
                allowed_tools=allowed_tools,
                llm_mode=llm_mode,
                record_llm_calls=record_llm_calls,
                obligation_id=obligation_id,
                agent=agent,
            )
            phase_runs = list((current_parent_run / "phase1B_runs").glob("*"))
            if phase_runs:
                current_parent_run = sorted(phase_runs)[-1]

        elif phase == "locate-client":
            if not current_parent_run:
                raise ValueError(f"Cannot run {phase} without previous phase output")
            if not client_repo:
                raise ValueError(f"Phase {phase} requires --client-repo")
            run_phase_2a(
                parent_run=current_parent_run,
                client_repo=client_repo,
                eip_number=eip,
                model=model,
                max_turns=max_turns,
                allowed_tools=allowed_tools,
                llm_mode=llm_mode,
                record_llm_calls=record_llm_calls,
                obligation_id=obligation_id,
                agent=agent,
            )
            phase_runs = list((current_parent_run / "phase2A_runs").glob("*"))
            if phase_runs:
                current_parent_run = sorted(phase_runs)[-1]

        elif phase == "analyze-client":
            if not current_parent_run:
                raise ValueError(f"Cannot run {phase} without previous phase output")
            if not client_repo:
                raise ValueError(f"Phase {phase} requires --client-repo")
            run_phase_2b(
                parent_run=current_parent_run,
                client_repo=client_repo,
                eip_number=eip,
                model=model,
                max_turns=max_turns,
                allowed_tools=allowed_tools,
                llm_mode=llm_mode,
                record_llm_calls=record_llm_calls,
                obligation_id=obligation_id,
                agent=agent,
            )
            # Last phase, no update needed

    # Generate report at the end
    print("\n=== Generating Report ===")
    write_report(run_root=run_root, output_dir=None, formats=["json", "md"])
    print(f"Pipeline completed. Report written to {run_root}/summary.md")
