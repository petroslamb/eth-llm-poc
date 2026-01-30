"""Phase runners for PoC 4.7."""

from __future__ import annotations

import csv
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from .agents import AgentProtocol
from .llm import ClaudeConfig, build_claude_config, config_metadata
from .prompts import load_prompt
from .spec_index import write_spec_index_bundle
from .utils import ensure_dir, timestamp


def normalize_eip_number(eip: Optional[str]) -> Optional[str]:
    if not eip:
        return None
    raw = str(eip).strip().lower()
    if raw.startswith("eip-"):
        raw = raw[4:]
    elif raw.startswith("eip"):
        raw = raw[3:]
    raw = raw.strip()
    if not raw:
        return None
    if not raw.isdigit():
        raise ValueError(f"EIP must be numeric or eip-<num>: {eip}")
    return raw


def infer_eip_number_from_path(path: Path) -> Optional[str]:
    match = re.search(r"eip-(\d+)\.md$", path.name, re.IGNORECASE)
    return match.group(1) if match else None


def infer_eip_number_from_csv(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            value = (row.get("id") or "").strip()
            match = re.match(r"EIP(\d+)-", value, re.IGNORECASE)
            if match:
                return match.group(1)
            break
    return None


def resolve_eip(eip_file: str, eip_number: Optional[str] = None) -> tuple[Path, str]:
    """Resolve EIP file path and number. Requires explicit file path."""
    path = Path(eip_file).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"EIP file not found: {path}")
    normalized = normalize_eip_number(eip_number) if eip_number else None
    if not normalized:
        inferred = infer_eip_number_from_path(path)
        if not inferred:
            raise ValueError(
                f"Unable to infer EIP number from {path.name}. Provide --eip."
            )
        normalized = inferred
    return path, normalized


def resolve_fork_root(
    spec_repo: str,
    fork: Optional[str] = None,
) -> tuple[Path, str]:
    """Resolve fork root directory. Requires explicit spec_repo path."""
    fork_name = (fork or "london").lower()
    spec_root = Path(spec_repo).expanduser().resolve()
    if not spec_root.exists():
        raise FileNotFoundError(f"Spec repo not found: {spec_root}")
    fork_root = spec_root / "src" / "ethereum" / "forks" / fork_name
    if not fork_root.exists():
        raise FileNotFoundError(f"Fork not found: {fork_root}")
    return fork_root.resolve(), fork_name


def resolve_client_root(client_repo: str) -> tuple[Path, str]:
    """Resolve client root directory. Requires explicit client_repo path."""
    path = Path(client_repo).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Client root not found: {path}")
    name = path.name or "client"
    return path, name


def eip_label(eip_number: str) -> str:
    return f"EIP-{eip_number}"


def eip_id_prefix(eip_number: str) -> str:
    return f"EIP{eip_number}"


def resolve_eip_number(
    eip_number: Optional[str],
    eip_path: Optional[Path] = None,
    input_csv: Optional[Path] = None,
) -> str:
    normalized = normalize_eip_number(eip_number) if eip_number else None
    if not normalized and eip_path:
        normalized = infer_eip_number_from_path(eip_path)
    if not normalized and input_csv:
        normalized = infer_eip_number_from_csv(input_csv)
    return normalized or "1559"


@dataclass(frozen=True)
class PhaseContext:
    phase: str
    input_csv: Optional[Path] = None
    output_csv: Optional[Path] = None
    eip_number: Optional[str] = None


def run_query(
    prompt: str,
    output_path: Path,
    cwd: Path,
    config: ClaudeConfig,
    agent: AgentProtocol,
    context: PhaseContext,
) -> None:
    agent.run(
        prompt,
        output_path,
        cwd,
        config,
        {
            "phase": context.phase,
            "input_csv": str(context.input_csv) if context.input_csv else None,
            "output_csv": str(context.output_csv) if context.output_csv else None,
            "eip_number": context.eip_number,
        },
    )


def write_prompt(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def copy_csv(source: Path, dest: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Input CSV not found: {source}")
    shutil.copy2(source, dest)


def run_phase_0a(
    eip_file: str,
    spec_repo: str,
    output_dir: str,
    eip_number: Optional[str] = None,
    model: Optional[str] = None,
    max_turns: int = 1,
    allowed_tools: Optional[Iterable[str]] = None,
    llm_mode: str = "live",
    record_llm_calls: bool = False,
    agent: Optional[AgentProtocol] = None,
) -> Path:
    """Run Phase 0A: Extract obligations from EIP.
    
    Args:
        eip_file: Path to the EIP markdown file (required)
        spec_repo: Path to execution-specs repo (required)
        output_dir: Directory for outputs (required)
        eip_number: EIP number (inferred from filename if not provided)
        model: Claude model identifier
        max_turns: Maximum turns per query
        allowed_tools: List of allowed tools for Claude
        llm_mode: 'live' or 'fake'
        record_llm_calls: Whether to record LLM call metadata
        agent: Agent implementation (defaults to ClaudeAgent)
    """
    from .agents import ClaudeAgent
    if agent is None:
        agent = ClaudeAgent()
    
    run_dir = Path(output_dir).expanduser().resolve() / "phase0A_runs" / timestamp()
    ensure_dir(run_dir)

    eip_path, resolved_eip_number = resolve_eip(eip_file, eip_number)
    resolved_eip_number = resolve_eip_number(resolved_eip_number, eip_path=eip_path)
    output_csv = run_dir / "obligations_index.csv"
    
    # Claude runs from the EIP file's parent directory
    cwd = eip_path.parent

    spec_outputs = write_spec_index_bundle(
        spec_repo=spec_repo,
        output_dir=str(run_dir),
        eip_fork_map_path=str(run_dir / "eip_fork_map.json"),
        spec_index_path=str(run_dir / "spec_index.json"),
        report_path=str(run_dir / "spec_index_report.md"),
    )

    config = build_claude_config(
        model,
        max_turns,
        allowed_tools,
        llm_mode=llm_mode,
        record_calls=record_llm_calls,
    )
    run_manifest = {
        "phase": "0A",
        "generated_at": timestamp(),
        "eip_number": resolved_eip_number,
        "eip_file": str(eip_path),
        "cwd": str(cwd),
        "spec_root": str(spec_outputs.spec_root),
        "spec_readme": str(spec_outputs.spec_readme),
        "spec_branch": spec_outputs.spec_branch,
        "spec_commit": spec_outputs.spec_commit,
        "spec_index": str(spec_outputs.spec_index_path),
        "eip_fork_map": str(spec_outputs.eip_fork_map_path),
        "spec_index_report": str(spec_outputs.report_path) if spec_outputs.report_path else None,
        "mismatch_forks": spec_outputs.mismatch_forks,
        "output_csv": str(output_csv),
        **config_metadata(config),
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2), encoding="utf-8"
    )

    prompt_template = load_prompt("phase0A_obligations")
    prompt = prompt_template.format(
        eip_path=eip_path,
        output_csv=output_csv,
        eip_label=eip_label(resolved_eip_number),
        eip_number=resolved_eip_number,
        eip_id_prefix=eip_id_prefix(resolved_eip_number),
    )

    prompt_path = run_dir / "phase0A_prompt.txt"
    output_path = run_dir / "phase0A_output.txt"

    write_prompt(prompt_path, prompt)
    run_query(
        prompt,
        output_path,
        cwd,
        config,
        agent,
        PhaseContext(
            phase="0A",
            output_csv=output_csv,
            eip_number=resolved_eip_number,
        ),
    )
    return run_dir


def run_phase_1a(
    parent_run: Path,
    spec_repo: str,
    eip_number: Optional[str] = None,
    fork: Optional[str] = None,
    model: Optional[str] = None,
    max_turns: int = 1,
    allowed_tools: Optional[Iterable[str]] = None,
    llm_mode: str = "live",
    record_llm_calls: bool = False,
    obligation_id: Optional[str] = None,
    agent: Optional[AgentProtocol] = None,
    spec_map_strict: bool = False,
) -> Path:
    """Run Phase 1A: Find spec locations for obligations.
    
    Args:
        parent_run: Path to Phase 0A run directory (required)
        spec_repo: Path to execution-specs repo (required)
        eip_number: EIP number (inferred from parent run if not provided)
        fork: Fork name (defaults to 'london')
        model: Claude model identifier
        max_turns: Maximum turns per query
        allowed_tools: List of allowed tools for Claude
        llm_mode: 'live' or 'fake'
        record_llm_calls: Whether to record LLM call metadata
        obligation_id: Limit to single obligation
        agent: Agent implementation (defaults to ClaudeAgent)
        spec_map_strict: Raise error on spec map mismatch
    """
    from .agents import ClaudeAgent
    if agent is None:
        agent = ClaudeAgent()
    
    run_dir = parent_run / "phase1A_runs" / timestamp()
    ensure_dir(run_dir)

    input_csv = parent_run / "obligations_index.csv"
    output_csv = run_dir / "obligations_index.csv"
    copy_csv(input_csv, output_csv)

    resolved_eip_number = resolve_eip_number(eip_number, input_csv=input_csv)
    fork_root, fork_name = resolve_fork_root(spec_repo, fork)
    
    # Claude runs from the spec repo root
    spec_root = Path(spec_repo).expanduser().resolve()
    cwd = spec_root

    spec_map_path = parent_run / "eip_fork_map.json"
    spec_map_check = {
        "fork": fork_name,
        "spec_map_path": str(spec_map_path),
        "status": "missing",
    }
    if spec_map_path.exists():
        try:
            data = json.loads(spec_map_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            spec_map_check["status"] = "invalid_json"
        else:
            entries = data.get("forks", [])
            entry = next(
                (
                    item
                    for item in entries
                    if str(item.get("fork", "")).lower() == fork_name.lower()
                ),
                None,
            )
            if entry is None:
                spec_map_check["status"] = "fork_not_found"
            else:
                mismatch = bool(entry.get("mismatch"))
                spec_map_check.update(
                    {
                        "status": "mismatch" if mismatch else "ok",
                        "readme_only": entry.get("readme_only", []),
                        "fork_init_only": entry.get("fork_init_only", []),
                        "mismatch": mismatch,
                    }
                )
                if mismatch and not spec_map_strict:
                    print(
                        f"[spec-map] WARNING fork '{fork_name}' mismatch: "
                        f"README-only {entry.get('readme_only')}, "
                        f"fork-only {entry.get('fork_init_only')}"
                    )

    spec_map_check_path = run_dir / "spec_map_check.json"
    spec_map_check_path.write_text(
        json.dumps(spec_map_check, indent=2), encoding="utf-8"
    )
    if spec_map_check.get("mismatch") and spec_map_strict:
        raise RuntimeError(
            f"Spec map mismatch for fork '{fork_name}'. "
            f"README-only: {spec_map_check.get('readme_only')}, "
            f"fork-only: {spec_map_check.get('fork_init_only')}"
        )

    config = build_claude_config(
        model,
        max_turns,
        allowed_tools,
        llm_mode=llm_mode,
        record_calls=record_llm_calls,
    )
    run_manifest = {
        "phase": "1A",
        "generated_at": timestamp(),
        "input_csv": str(input_csv),
        "output_csv": str(output_csv),
        "eip_number": resolved_eip_number,
        "fork_name": fork_name,
        "fork_root": str(fork_root),
        "spec_repo": str(spec_root),
        "cwd": str(cwd),
        "spec_map_check": str(spec_map_check_path),
        "obligation_id": obligation_id,
        "parent_run": str(parent_run),
        **config_metadata(config),
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2), encoding="utf-8"
    )
    prompt_template = load_prompt("phase1A_locations")
    prompt = prompt_template.format(
        input_csv=input_csv,
        output_csv=output_csv,
        spec_root=fork_root,
        fork_name=fork_name,
        eip_label=eip_label(resolved_eip_number),
    )
    if obligation_id:
        prompt += (
            f"\n\nOnly update the row with id '{obligation_id}'. "
            "Leave all other rows unchanged.\n"
        )

    prompt_path = run_dir / "phase1A_prompt.txt"
    output_path = run_dir / "phase1A_output.txt"

    write_prompt(prompt_path, prompt)
    run_query(
        prompt,
        output_path,
        cwd,
        config,
        agent,
        PhaseContext(
            phase="1A",
            input_csv=input_csv,
            output_csv=output_csv,
            eip_number=resolved_eip_number,
        ),
    )
    return run_dir


def run_phase_1b(
    parent_run: Path,
    spec_repo: Optional[str] = None,
    eip_number: Optional[str] = None,
    model: Optional[str] = None,
    max_turns: int = 1,
    allowed_tools: Optional[Iterable[str]] = None,
    llm_mode: str = "live",
    record_llm_calls: bool = False,
    obligation_id: Optional[str] = None,
    agent: Optional[AgentProtocol] = None,
) -> Path:
    """Run Phase 1B: Analyze code flow for obligations.
    
    Args:
        parent_run: Path to Phase 1A run directory (required)
        spec_repo: Path to execution-specs repo (inferred from parent manifest if not provided)
        eip_number: EIP number (inferred from parent run if not provided)
        model: Claude model identifier
        max_turns: Maximum turns per query
        allowed_tools: List of allowed tools for Claude
        llm_mode: 'live' or 'fake'
        record_llm_calls: Whether to record LLM call metadata
        obligation_id: Limit to single obligation
        agent: Agent implementation (defaults to ClaudeAgent)
    """
    from .agents import ClaudeAgent
    if agent is None:
        agent = ClaudeAgent()
    
    run_dir = parent_run / "phase1B_runs" / timestamp()
    ensure_dir(run_dir)

    input_csv = parent_run / "obligations_index.csv"
    output_csv = run_dir / "obligations_index.csv"
    copy_csv(input_csv, output_csv)

    # Infer spec_repo from parent manifest if not provided
    if not spec_repo:
        parent_manifest = parent_run / "run_manifest.json"
        if parent_manifest.exists():
            try:
                manifest_data = json.loads(parent_manifest.read_text(encoding="utf-8"))
                spec_repo = manifest_data.get("spec_repo")
            except (json.JSONDecodeError, KeyError):
                pass
    
    if not spec_repo:
        raise ValueError("spec_repo is required: provide --spec-repo or ensure parent run manifest contains spec_repo")
    
    # Claude runs from the spec repo root
    cwd = Path(spec_repo).expanduser().resolve()

    resolved_eip_number = resolve_eip_number(eip_number, input_csv=input_csv)
    prompt_template = load_prompt("phase1B_codeflow")
    prompt = prompt_template.format(
        input_csv=input_csv,
        output_csv=output_csv,
        eip_label=eip_label(resolved_eip_number),
    )
    if obligation_id:
        prompt += (
            f"\n\nOnly update the row with id '{obligation_id}'. "
            "Leave all other rows unchanged.\n"
        )

    config = build_claude_config(
        model,
        max_turns,
        allowed_tools,
        llm_mode=llm_mode,
        record_calls=record_llm_calls,
    )
    run_manifest = {
        "phase": "1B",
        "generated_at": timestamp(),
        "input_csv": str(input_csv),
        "output_csv": str(output_csv),
        "eip_number": resolved_eip_number,
        "spec_repo": str(cwd),
        "cwd": str(cwd),
        "obligation_id": obligation_id,
        "parent_run": str(parent_run),
        **config_metadata(config),
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2), encoding="utf-8"
    )

    prompt_path = run_dir / "phase1B_prompt.txt"
    output_path = run_dir / "phase1B_output.txt"

    write_prompt(prompt_path, prompt)
    run_query(
        prompt,
        output_path,
        cwd,
        config,
        agent,
        PhaseContext(
            phase="1B",
            input_csv=input_csv,
            output_csv=output_csv,
            eip_number=resolved_eip_number,
        ),
    )
    return run_dir


def run_phase_2a(
    parent_run: Path,
    client_repo: str,
    eip_number: Optional[str] = None,
    model: Optional[str] = None,
    max_turns: int = 1,
    allowed_tools: Optional[Iterable[str]] = None,
    llm_mode: str = "live",
    record_llm_calls: bool = False,
    obligation_id: Optional[str] = None,
    agent: Optional[AgentProtocol] = None,
) -> Path:
    """Run Phase 2A: Find client locations for obligations.
    
    Args:
        parent_run: Path to Phase 1B run directory (required)
        client_repo: Path to client repo (e.g., geth) (required)
        eip_number: EIP number (inferred from parent run if not provided)
        model: Claude model identifier
        max_turns: Maximum turns per query
        allowed_tools: List of allowed tools for Claude
        llm_mode: 'live' or 'fake'
        record_llm_calls: Whether to record LLM call metadata
        obligation_id: Limit to single obligation
        agent: Agent implementation (defaults to ClaudeAgent)
    """
    from .agents import ClaudeAgent
    if agent is None:
        agent = ClaudeAgent()
    
    run_dir = parent_run / "phase2A_runs" / timestamp()
    ensure_dir(run_dir)

    input_csv = parent_run / "obligations_index.csv"
    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")
    output_csv = run_dir / "client_obligations_index.csv"

    resolved_eip_number = resolve_eip_number(eip_number, input_csv=input_csv)
    resolved_client_root, resolved_client_name = resolve_client_root(client_repo)
    
    # Claude runs from the client repo root
    cwd = resolved_client_root
    
    prompt_template = load_prompt("phase2A_client_locations")
    prompt = prompt_template.format(
        input_csv=input_csv,
        output_csv=output_csv,
        client_root=resolved_client_root,
        client_name=resolved_client_name,
        eip_label=eip_label(resolved_eip_number),
        eip_number=resolved_eip_number,
    )
    if obligation_id:
        prompt += (
            f"\n\nOnly update the row with id '{obligation_id}'. "
            "Leave all other rows unchanged.\n"
        )

    config = build_claude_config(
        model,
        max_turns,
        allowed_tools,
        llm_mode=llm_mode,
        record_calls=record_llm_calls,
    )
    run_manifest = {
        "phase": "2A",
        "generated_at": timestamp(),
        "input_csv": str(input_csv),
        "output_csv": str(output_csv),
        "eip_number": resolved_eip_number,
        "client_name": resolved_client_name,
        "client_root": str(resolved_client_root),
        "cwd": str(cwd),
        "obligation_id": obligation_id,
        "parent_run": str(parent_run),
        **config_metadata(config),
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2), encoding="utf-8"
    )

    prompt_path = run_dir / "phase2A_prompt.txt"
    output_path = run_dir / "phase2A_output.txt"

    write_prompt(prompt_path, prompt)
    run_query(
        prompt,
        output_path,
        cwd,
        config,
        agent,
        PhaseContext(
            phase="2A",
            input_csv=input_csv,
            output_csv=output_csv,
            eip_number=resolved_eip_number,
        ),
    )
    return run_dir


def run_phase_2b(
    parent_run: Path,
    client_repo: str,
    eip_number: Optional[str] = None,
    model: Optional[str] = None,
    max_turns: int = 1,
    allowed_tools: Optional[Iterable[str]] = None,
    llm_mode: str = "live",
    record_llm_calls: bool = False,
    obligation_id: Optional[str] = None,
    agent: Optional[AgentProtocol] = None,
) -> Path:
    """Run Phase 2B: Identify gaps in client implementation.
    
    Args:
        parent_run: Path to Phase 2A run directory (required)
        client_repo: Path to client repo (e.g., geth) (required)
        eip_number: EIP number (inferred from parent run if not provided)
        model: Claude model identifier
        max_turns: Maximum turns per query
        allowed_tools: List of allowed tools for Claude
        llm_mode: 'live' or 'fake'
        record_llm_calls: Whether to record LLM call metadata
        obligation_id: Limit to single obligation
        agent: Agent implementation (defaults to ClaudeAgent)
    """
    from .agents import ClaudeAgent
    if agent is None:
        agent = ClaudeAgent()
    
    run_dir = parent_run / "phase2B_runs" / timestamp()
    ensure_dir(run_dir)

    input_csv = parent_run / "client_obligations_index.csv"
    output_csv = run_dir / "client_obligations_index.csv"
    copy_csv(input_csv, output_csv)

    resolved_eip_number = resolve_eip_number(eip_number, input_csv=input_csv)
    resolved_client_root, resolved_client_name = resolve_client_root(client_repo)
    
    # Claude runs from the client repo root
    cwd = resolved_client_root
    
    prompt_template = load_prompt("phase2B_client_gaps")
    prompt = prompt_template.format(
        input_csv=input_csv,
        output_csv=output_csv,
        client_root=resolved_client_root,
        client_name=resolved_client_name,
        eip_label=eip_label(resolved_eip_number),
        eip_number=resolved_eip_number,
    )
    if obligation_id:
        prompt += (
            f"\n\nOnly update the row with id '{obligation_id}'. "
            "Leave all other rows unchanged.\n"
        )

    config = build_claude_config(
        model,
        max_turns,
        allowed_tools,
        llm_mode=llm_mode,
        record_calls=record_llm_calls,
    )
    run_manifest = {
        "phase": "2B",
        "generated_at": timestamp(),
        "input_csv": str(input_csv),
        "output_csv": str(output_csv),
        "eip_number": resolved_eip_number,
        "client_name": resolved_client_name,
        "client_root": str(resolved_client_root),
        "cwd": str(cwd),
        "obligation_id": obligation_id,
        "parent_run": str(parent_run),
        **config_metadata(config),
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2), encoding="utf-8"
    )

    prompt_path = run_dir / "phase2B_prompt.txt"
    output_path = run_dir / "phase2B_output.txt"

    write_prompt(prompt_path, prompt)
    run_query(
        prompt,
        output_path,
        cwd,
        config,
        agent,
        PhaseContext(
            phase="2B",
            input_csv=input_csv,
            output_csv=output_csv,
            eip_number=resolved_eip_number,
        ),
    )
    return run_dir
