"""Spec indexing utilities for execution-specs."""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .utils import ensure_dir, notes_root, timestamp


TABLE_HEADER = "### Ethereum Protocol Releases"


@dataclass(frozen=True)
class GitInfo:
    branch: Optional[str]
    commit: Optional[str]


@dataclass(frozen=True)
class SpecIndexOutputs:
    root_dir: Path
    spec_root: Path
    spec_readme: Path
    spec_branch: Optional[str]
    spec_commit: Optional[str]
    eip_fork_map_path: Path
    spec_index_path: Path
    report_path: Optional[Path]
    mismatch_forks: list[str]


def _run_git(path: Path, args: list[str]) -> Optional[str]:
    try:
        result = subprocess.check_output(
            ["git", "-C", str(path), *args],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    value = result.strip()
    return value or None


def get_git_info(repo_path: Path) -> GitInfo:
    branch = _run_git(repo_path, ["rev-parse", "--abbrev-ref", "HEAD"])
    commit = _run_git(repo_path, ["rev-parse", "HEAD"])
    return GitInfo(branch=branch, commit=commit)


def extract_table_rows(text: str) -> list[str]:
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.strip() == TABLE_HEADER:
            start = idx + 1
            break
    if start is None:
        raise ValueError(f"Table header not found: {TABLE_HEADER}")

    rows: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("|"):
            rows.append(line)
            continue
        if rows:
            break
    return rows


def parse_release_table(rows: list[str], spec_root: Optional[Path]) -> list[dict[str, object]]:
    forks: list[dict[str, object]] = []
    for row in rows:
        if re.match(r"^\|\s*-+", row):
            continue
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if not cells or len(cells) < 2:
            continue
        fork = cells[0]
        eips_readme = sorted({int(num) for num in re.findall(r"EIP-(\d+)", row)})
        spec_path_match = re.search(r"(/src/ethereum/forks/[^)\s]+)", row)
        spec_path = spec_path_match.group(1) if spec_path_match else None

        eips_fork_init: list[int] | None = None
        if spec_root is not None and spec_path is not None:
            fork_init_path = spec_root / spec_path.lstrip("/")
            if fork_init_path.exists():
                text = fork_init_path.read_text(encoding="utf-8")
                eips_fork_init = sorted(
                    {int(num) for num in re.findall(r"EIP-(\d+)", text)}
                )

        eips_readme_set = set(eips_readme)
        eips_fork_set = set(eips_fork_init or [])
        readme_only = sorted(eips_readme_set - eips_fork_set) if eips_fork_init else []
        fork_only = sorted(eips_fork_set - eips_readme_set) if eips_fork_init else []
        mismatch = bool(readme_only or fork_only)

        forks.append(
            {
                "fork": fork,
                "spec_path": spec_path,
                "eips_readme": eips_readme,
                "eips_fork_init": eips_fork_init,
                "readme_only": readme_only,
                "fork_init_only": fork_only,
                "mismatch": mismatch,
            }
        )
    return forks


def build_eip_fork_map(readme_path: Path, spec_root: Optional[Path]) -> dict[str, object]:
    text = readme_path.read_text(encoding="utf-8")
    rows = extract_table_rows(text)
    forks = parse_release_table(rows, spec_root)
    return {
        "source": str(readme_path),
        "spec_root": str(spec_root) if spec_root else None,
        "forks": forks,
    }


def write_spec_index_report(report_path: Path, eip_fork_map: dict[str, object], git_info: GitInfo) -> None:
    forks = eip_fork_map.get("forks", [])
    mismatches = [entry for entry in forks if entry.get("mismatch")]
    lines = [
        "# Spec Index Report",
        "",
        f"- Spec branch: {git_info.branch or 'unknown'}",
        f"- Spec commit: {git_info.commit or 'unknown'}",
        f"- Total forks parsed: {len(forks)}",
        f"- Forks with README vs __init__ mismatches: {len(mismatches)}",
        "",
    ]
    if mismatches:
        lines.append("## Mismatches")
        for entry in mismatches:
            fork = entry.get("fork")
            readme_only = entry.get("readme_only") or []
            fork_only = entry.get("fork_init_only") or []
            lines.append(f"- {fork}: README-only {readme_only}, fork-only {fork_only}")
        lines.append("")
    else:
        lines.append("No mismatches detected between README and fork __init__.py EIP lists.")
        lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_spec_index_bundle(
    repo_root: Path,
    spec_root: Optional[str],
    spec_readme: Optional[str],
    output_dir: Optional[str],
    eip_fork_map_path: Optional[str],
    spec_index_path: Optional[str],
    report_path: Optional[str],
) -> SpecIndexOutputs:
    resolved_spec_root = (
        Path(spec_root).expanduser().resolve()
        if spec_root
        else (repo_root / "specs" / "execution-specs").resolve()
    )
    readme_path = (
        Path(spec_readme).expanduser().resolve()
        if spec_readme
        else resolved_spec_root / "README.md"
    )
    if not readme_path.exists():
        raise FileNotFoundError(f"Spec README not found: {readme_path}")

    root_dir = (
        Path(output_dir).expanduser().resolve()
        if output_dir
        else (notes_root(repo_root) / "index_runs" / timestamp())
    )
    ensure_dir(root_dir)

    eip_fork_map_file = (
        Path(eip_fork_map_path).expanduser().resolve()
        if eip_fork_map_path
        else root_dir / "eip_fork_map.json"
    )
    spec_index_file = (
        Path(spec_index_path).expanduser().resolve()
        if spec_index_path
        else root_dir / "spec_index.json"
    )
    report_file = (
        Path(report_path).expanduser().resolve()
        if report_path
        else root_dir / "spec_index_report.md"
    )

    git_info = get_git_info(resolved_spec_root)
    eip_fork_map = build_eip_fork_map(readme_path, resolved_spec_root)
    eip_fork_map_file.write_text(json.dumps(eip_fork_map, indent=2), encoding="utf-8")

    mismatches = [
        entry["fork"]
        for entry in eip_fork_map["forks"]
        if entry.get("mismatch")
    ]

    spec_index = {
        "generated_at": timestamp(),
        "spec_root": str(resolved_spec_root),
        "spec_readme": str(readme_path),
        "spec_branch": git_info.branch,
        "spec_commit": git_info.commit,
        "forks": eip_fork_map["forks"],
    }
    spec_index_file.write_text(json.dumps(spec_index, indent=2), encoding="utf-8")

    write_spec_index_report(report_file, eip_fork_map, git_info)

    return SpecIndexOutputs(
        root_dir=root_dir,
        spec_root=resolved_spec_root,
        spec_readme=readme_path,
        spec_branch=git_info.branch,
        spec_commit=git_info.commit,
        eip_fork_map_path=eip_fork_map_file,
        spec_index_path=spec_index_file,
        report_path=report_file,
        mismatch_forks=mismatches,
    )


def run_index_specs(
    repo_root: Path,
    spec_root: Optional[str],
    spec_readme: Optional[str],
    output_dir: Optional[str],
    eip_fork_map_path: Optional[str],
    spec_index_path: Optional[str],
    run_manifest_path: Optional[str],
) -> Path:
    outputs = write_spec_index_bundle(
        repo_root=repo_root,
        spec_root=spec_root,
        spec_readme=spec_readme,
        output_dir=output_dir,
        eip_fork_map_path=eip_fork_map_path,
        spec_index_path=spec_index_path,
        report_path=None,
    )
    run_manifest_file = (
        Path(run_manifest_path).expanduser().resolve()
        if run_manifest_path
        else outputs.root_dir / "run_manifest.json"
    )
    run_manifest = {
        "generated_at": timestamp(),
        "spec_root": str(outputs.spec_root),
        "spec_readme": str(outputs.spec_readme),
        "spec_branch": outputs.spec_branch,
        "spec_commit": outputs.spec_commit,
        "spec_index": str(outputs.spec_index_path),
        "eip_fork_map": str(outputs.eip_fork_map_path),
        "spec_index_report": str(outputs.report_path) if outputs.report_path else None,
        "mismatch_forks": outputs.mismatch_forks,
    }
    run_manifest_file.write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")
    return outputs.root_dir
