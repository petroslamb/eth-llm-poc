"""Phase runners for PoC 4.7."""

from __future__ import annotations

import csv
import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import anyio

from .prompts import load_prompt
from .spec_index import write_spec_index_bundle
from .utils import ensure_dir, notes_root, timestamp


DEFAULT_ALLOWED_TOOLS = ["Read", "Write", "Bash", "Grep", "Glob"]


@dataclass(frozen=True)
class ClaudeConfig:
    model: Optional[str]
    max_turns: int
    allowed_tools: list[str]
    llm_mode: str = "live"
    record_calls: bool = False
    stub_response_path: Optional[Path] = None


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


def resolve_eip(repo_root: Path, eip_file: Optional[str], eip_number: Optional[str]) -> tuple[Path, str]:
    normalized = normalize_eip_number(eip_number) if eip_number else None
    if eip_file:
        path = Path(eip_file).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"EIP file not found: {path}")
        if not normalized:
            inferred = infer_eip_number_from_path(path)
            if not inferred:
                raise ValueError(
                    f"Unable to infer EIP number from {path.name}. Provide --eip."
                )
            normalized = inferred
        return path, normalized

    if not normalized:
        normalized = "1559"

    filename = f"eip-{normalized}.md"
    specs_root = repo_root / "specs"
    candidates = []
    if specs_root.exists():
        candidates.extend(specs_root.rglob(filename))
    if not candidates:
        candidates.extend(repo_root.rglob(filename))
    if not candidates:
        raise FileNotFoundError(f"Could not locate {filename}. Provide --eip-file.")
    return candidates[0].resolve(), normalized


def resolve_fork_root(
    repo_root: Path,
    fork: Optional[str],
    spec_root: Optional[str],
) -> tuple[Path, str]:
    if spec_root:
        path = Path(spec_root).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Spec fork root not found: {path}")
        fork_name = fork or path.name
        return path, fork_name

    fork_name = (fork or "london").lower()
    fork_root = (
        repo_root / "specs" / "execution-specs" / "src" / "ethereum" / "forks" / fork_name
    )
    if not fork_root.exists():
        raise FileNotFoundError(f"Fork not found: {fork_root}")
    return fork_root.resolve(), fork_name


def resolve_client_root(
    repo_root: Path,
    client_name: Optional[str],
    client_root: Optional[str],
) -> tuple[Path, str]:
    name = (client_name or "geth").strip()
    if client_root:
        path = Path(client_root).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Client root not found: {path}")
        return path, name

    default_root = repo_root / "clients" / "execution" / name
    if not default_root.exists():
        raise FileNotFoundError(f"Client root not found: {default_root}")
    return default_root.resolve(), name


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


def build_claude_config(
    model: Optional[str],
    max_turns: int,
    allowed_tools: Optional[Iterable[str]],
    llm_mode: str = "live",
    record_calls: bool = False,
    stub_response_path: Optional[str] = None,
) -> ClaudeConfig:
    tools = list(allowed_tools) if allowed_tools else DEFAULT_ALLOWED_TOOLS
    stub_path = Path(stub_response_path).expanduser().resolve() if stub_response_path else None
    return ClaudeConfig(
        model=model,
        max_turns=max_turns,
        allowed_tools=tools,
        llm_mode=llm_mode,
        record_calls=record_calls,
        stub_response_path=stub_path,
    )


def write_llm_call_record(
    *,
    output_path: Path,
    prompt: str,
    options_kwargs: dict[str, object],
    config: ClaudeConfig,
    used_stub: bool,
) -> Path:
    record_path = output_path.with_suffix(".call.json")
    record = {
        "recorded_at": timestamp(),
        "llm_mode": config.llm_mode,
        "used_stub": used_stub,
        "prompt": prompt,
        "options": options_kwargs,
        "stub_response_path": str(config.stub_response_path) if config.stub_response_path else None,
        "output_path": str(output_path),
    }
    record_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record_path


async def _run_query(prompt: str, output_path: Path, repo_root: Path, config: ClaudeConfig) -> None:
    options_kwargs = {
        "allowed_tools": config.allowed_tools,
        "permission_mode": "bypassPermissions",
        "max_turns": config.max_turns,
        "cwd": str(repo_root),
    }
    if config.model:
        options_kwargs["model"] = config.model

    if config.llm_mode == "stub":
        write_llm_call_record(
            output_path=output_path,
            prompt=prompt,
            options_kwargs=options_kwargs,
            config=config,
            used_stub=True,
        )
        if config.stub_response_path and config.stub_response_path.exists():
            output_text = config.stub_response_path.read_text(encoding="utf-8")
        else:
            output_text = (
                "STUB MODE: Claude call skipped.\n"
                f"Recorded call metadata in {output_path.with_suffix('.call.json').name}.\n"
            )
        output_path.write_text(output_text, encoding="utf-8")
        return

    if not (os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")):
        raise RuntimeError(
            "Missing API credentials. Set ANTHROPIC_API_KEY (or ANTHROPIC_AUTH_TOKEN) "
            "in your environment before running."
        )
    try:
        from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock, query
    except ModuleNotFoundError as exc:  # pragma: no cover - runtime dependency
        raise RuntimeError(
            "claude_agent_sdk is not installed. Install it with: uv pip install claude-agent-sdk"
        ) from exc

    options = ClaudeAgentOptions(**options_kwargs)
    if config.record_calls:
        write_llm_call_record(
            output_path=output_path,
            prompt=prompt,
            options_kwargs=options_kwargs,
            config=config,
            used_stub=False,
        )

    text_chunks: list[str] = []
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text_chunks.append(block.text)

    output_path.write_text("".join(text_chunks), encoding="utf-8")


def run_query(prompt: str, output_path: Path, repo_root: Path, config: ClaudeConfig) -> None:
    anyio.run(_run_query, prompt, output_path, repo_root, config)


def write_prompt(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def copy_csv(source: Path, dest: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Input CSV not found: {source}")
    shutil.copy2(source, dest)


def run_phase_0a(
    repo_root: Path,
    eip_file: Optional[str],
    eip_number: Optional[str],
    model: Optional[str],
    max_turns: int,
    allowed_tools: Optional[Iterable[str]],
    llm_mode: str,
    record_llm_calls: bool,
    stub_response_path: Optional[str],
) -> Path:
    root_ts = timestamp()
    root_dir = notes_root(repo_root) / root_ts
    run_dir = root_dir / "phase0A_runs" / timestamp()
    ensure_dir(run_dir)

    eip_path, resolved_eip_number = resolve_eip(repo_root, eip_file, eip_number)
    resolved_eip_number = resolve_eip_number(resolved_eip_number, eip_path=eip_path)
    output_csv = run_dir / "obligations_index.csv"

    spec_outputs = write_spec_index_bundle(
        repo_root=repo_root,
        spec_root=None,
        spec_readme=None,
        output_dir=str(run_dir),
        eip_fork_map_path=str(run_dir / "eip_fork_map.json"),
        spec_index_path=str(run_dir / "spec_index.json"),
        report_path=str(run_dir / "spec_index_report.md"),
    )

    run_manifest = {
        "phase": "0A",
        "generated_at": timestamp(),
        "eip_number": resolved_eip_number,
        "eip_file": str(eip_path),
        "spec_root": str(spec_outputs.spec_root),
        "spec_readme": str(spec_outputs.spec_readme),
        "spec_branch": spec_outputs.spec_branch,
        "spec_commit": spec_outputs.spec_commit,
        "spec_index": str(spec_outputs.spec_index_path),
        "eip_fork_map": str(spec_outputs.eip_fork_map_path),
        "spec_index_report": str(spec_outputs.report_path) if spec_outputs.report_path else None,
        "mismatch_forks": spec_outputs.mismatch_forks,
        "output_csv": str(output_csv),
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
    config = build_claude_config(
        model,
        max_turns,
        allowed_tools,
        llm_mode=llm_mode,
        record_calls=record_llm_calls,
        stub_response_path=stub_response_path,
    )
    run_query(prompt, output_path, repo_root, config)
    return run_dir


def run_phase_1a(
    repo_root: Path,
    parent_run: Path,
    eip_number: Optional[str],
    fork: Optional[str],
    spec_root: Optional[str],
    model: Optional[str],
    max_turns: int,
    allowed_tools: Optional[Iterable[str]],
    llm_mode: str,
    record_llm_calls: bool,
    stub_response_path: Optional[str],
    obligation_id: Optional[str],
    spec_map_strict: bool = False,
) -> Path:
    run_dir = parent_run / "phase1A_runs" / timestamp()
    ensure_dir(run_dir)

    input_csv = parent_run / "obligations_index.csv"
    output_csv = run_dir / "obligations_index.csv"
    copy_csv(input_csv, output_csv)

    resolved_eip_number = resolve_eip_number(eip_number, input_csv=input_csv)
    fork_root, fork_name = resolve_fork_root(repo_root, fork, spec_root)

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

    run_manifest = {
        "phase": "1A",
        "generated_at": timestamp(),
        "input_csv": str(input_csv),
        "output_csv": str(output_csv),
        "eip_number": resolved_eip_number,
        "fork_name": fork_name,
        "fork_root": str(fork_root),
        "spec_map_check": str(spec_map_check_path),
        "spec_map_strict": spec_map_strict,
        "parent_run": str(parent_run),
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
    config = build_claude_config(
        model,
        max_turns,
        allowed_tools,
        llm_mode=llm_mode,
        record_calls=record_llm_calls,
        stub_response_path=stub_response_path,
    )
    run_query(prompt, output_path, repo_root, config)
    return run_dir


def run_phase_1b(
    repo_root: Path,
    parent_run: Path,
    eip_number: Optional[str],
    model: Optional[str],
    max_turns: int,
    allowed_tools: Optional[Iterable[str]],
    llm_mode: str,
    record_llm_calls: bool,
    stub_response_path: Optional[str],
    obligation_id: Optional[str],
) -> Path:
    run_dir = parent_run / "phase1B_runs" / timestamp()
    ensure_dir(run_dir)

    input_csv = parent_run / "obligations_index.csv"
    output_csv = run_dir / "obligations_index.csv"
    copy_csv(input_csv, output_csv)

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

    run_manifest = {
        "phase": "1B",
        "generated_at": timestamp(),
        "input_csv": str(input_csv),
        "output_csv": str(output_csv),
        "eip_number": resolved_eip_number,
        "parent_run": str(parent_run),
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2), encoding="utf-8"
    )

    prompt_path = run_dir / "phase1B_prompt.txt"
    output_path = run_dir / "phase1B_output.txt"

    write_prompt(prompt_path, prompt)
    config = build_claude_config(
        model,
        max_turns,
        allowed_tools,
        llm_mode=llm_mode,
        record_calls=record_llm_calls,
        stub_response_path=stub_response_path,
    )
    run_query(prompt, output_path, repo_root, config)
    return run_dir


def run_phase_2a(
    repo_root: Path,
    parent_run: Path,
    eip_number: Optional[str],
    client_name: Optional[str],
    client_root: Optional[str],
    model: Optional[str],
    max_turns: int,
    allowed_tools: Optional[Iterable[str]],
    llm_mode: str,
    record_llm_calls: bool,
    stub_response_path: Optional[str],
    obligation_id: Optional[str],
) -> Path:
    run_dir = parent_run / "phase2A_runs" / timestamp()
    ensure_dir(run_dir)

    input_csv = parent_run / "obligations_index.csv"
    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")
    output_csv = run_dir / "client_obligations_index.csv"

    resolved_eip_number = resolve_eip_number(eip_number, input_csv=input_csv)
    resolved_client_root, resolved_client_name = resolve_client_root(
        repo_root, client_name, client_root
    )
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

    run_manifest = {
        "phase": "2A",
        "generated_at": timestamp(),
        "input_csv": str(input_csv),
        "output_csv": str(output_csv),
        "eip_number": resolved_eip_number,
        "client_name": resolved_client_name,
        "client_root": str(resolved_client_root),
        "parent_run": str(parent_run),
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2), encoding="utf-8"
    )

    prompt_path = run_dir / "phase2A_prompt.txt"
    output_path = run_dir / "phase2A_output.txt"

    write_prompt(prompt_path, prompt)
    config = build_claude_config(
        model,
        max_turns,
        allowed_tools,
        llm_mode=llm_mode,
        record_calls=record_llm_calls,
        stub_response_path=stub_response_path,
    )
    run_query(prompt, output_path, repo_root, config)
    return run_dir


def run_phase_2b(
    repo_root: Path,
    parent_run: Path,
    eip_number: Optional[str],
    client_name: Optional[str],
    client_root: Optional[str],
    model: Optional[str],
    max_turns: int,
    allowed_tools: Optional[Iterable[str]],
    llm_mode: str,
    record_llm_calls: bool,
    stub_response_path: Optional[str],
    obligation_id: Optional[str],
) -> Path:
    run_dir = parent_run / "phase2B_runs" / timestamp()
    ensure_dir(run_dir)

    input_csv = parent_run / "client_obligations_index.csv"
    output_csv = run_dir / "client_obligations_index.csv"
    copy_csv(input_csv, output_csv)

    resolved_eip_number = resolve_eip_number(eip_number, input_csv=input_csv)
    resolved_client_root, resolved_client_name = resolve_client_root(
        repo_root, client_name, client_root
    )
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

    run_manifest = {
        "phase": "2B",
        "generated_at": timestamp(),
        "input_csv": str(input_csv),
        "output_csv": str(output_csv),
        "eip_number": resolved_eip_number,
        "client_name": resolved_client_name,
        "client_root": str(resolved_client_root),
        "parent_run": str(parent_run),
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2), encoding="utf-8"
    )

    prompt_path = run_dir / "phase2B_prompt.txt"
    output_path = run_dir / "phase2B_output.txt"

    write_prompt(prompt_path, prompt)
    config = build_claude_config(
        model,
        max_turns,
        allowed_tools,
        llm_mode=llm_mode,
        record_calls=record_llm_calls,
        stub_response_path=stub_response_path,
    )
    run_query(prompt, output_path, repo_root, config)
    return run_dir
