"""Pipeline orchestration for multi-phase verification."""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

from contextlib import contextmanager

from .agents import AgentProtocol, ClaudeAgent
from .reporting import write_report
from .runner import run_phase_0a, run_phase_1a, run_phase_1b, run_phase_2a, run_phase_2b
from .utils import timestamp


@contextmanager
def github_log_group(title: str):
    """Wrap logs in a GitHub Actions group if running in CI."""
    is_ci = os.getenv("GITHUB_ACTIONS") == "true"
    if is_ci:
        print(f"::group::{title}")
    try:
        yield
    finally:
        if is_ci:
            print("::endgroup::")



PHASE_ORDER = ["extract", "locate-spec", "analyze-spec", "locate-client", "analyze-client"]



def _log_phase_to_summary(phase: str, run_dir: Path) -> None:
    """Append phase artifacts (prompt/output) to GitHub Step Summary."""
    step_summary = os.getenv("GITHUB_STEP_SUMMARY")
    if not step_summary:
        return

    # Find prompt and output files. 
    # Usually locally named 'prompt.txt' or similar inside the run_dir.
    # The runner saves them directly in run_dir as phase is leaf.
    
    # We'll look for common patterns or just list .txt files if needed.
    # But usually runners produce: {phase}_prompt.txt and {phase}_output.txt OR just prompt.txt
    # Looking at runner.py, it seems varied.
    # Phase 0A: writes to `run_manifest` but not always text files? 
    # Actually, the llm agent `run()` method saves `prompt.txt` and `response.txt` usually?
    # No, `ClaudeAgent.run` saves `*_prompt.txt` and `*_call.json` and `*_output.txt`? 
    # Let's just look for any .txt file that isn't empty.
    
    # Better approach: check specifically for likely artifact names based on common patterns
    # or just list prompt/output files.
    
    artifacts = []
    
    # Simple heuristic: look for *prompt.txt and *output.txt
    for path in sorted(run_dir.glob("*.txt")):
        if "prompt" in path.name or "output" in path.name:
            artifacts.append(path)
            
    if not artifacts:
        return

    try:
        with open(step_summary, "a", encoding="utf-8") as f:
            f.write(f"\n<details>\n<summary>Phase {phase} Artifacts</summary>\n\n")
            
            for art in artifacts:
                name = art.name
                content = art.read_text(encoding="utf-8", errors="replace")
                
                # Truncate to 20KB
                MAX_SIZE = 20 * 1024
                if len(content) > MAX_SIZE:
                    content = content[:MAX_SIZE] + "\n... (Truncated)"
                
                f.write(f"#### {name}\n")
                f.write("```text\n")
                f.write(content)
                f.write("\n```\n\n")
                
            f.write("</details>\n")
    except Exception as e:
        print(f"Failed to write to step summary: {e}")


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

        with github_log_group(f"Phase: {phase}"):
            print(f"\n=== Running Phase: {phase} ===")
        
        phase_output_dir = None

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
                phase_output_dir = current_parent_run
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
                phase_output_dir = current_parent_run

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
                phase_output_dir = current_parent_run

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
                phase_output_dir = current_parent_run

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
            # Last phase, no update needed to current_parent_run logically for next step, 
            # but we define phase_output_dir for logging.
            # Usually it's in phase2B_runs/timestamp
            phase_runs = list((current_parent_run / "phase2B_runs").glob("*"))
            if phase_runs:
                phase_output_dir = sorted(phase_runs)[-1]
        
        # Log to GitHub Step Summary if running in Actions
        if phase_output_dir:
            _log_phase_to_summary(phase, phase_output_dir)

    # Generate report at the end
    print("\n=== Generating Report ===")
    write_report(run_root=run_root, output_dir=None, formats=["json", "md"])
    print(f"Pipeline completed. Report written to {run_root}/summary.md")

    # Write to GitHub Step Summary if running in Actions
    step_summary = os.getenv("GITHUB_STEP_SUMMARY")
    if step_summary:
        summary_md = run_root / "summary.md"
        if summary_md.exists():
            with open(step_summary, "a", encoding="utf-8") as f:
                f.write(summary_md.read_text(encoding="utf-8"))
