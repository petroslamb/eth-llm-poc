"""Run report aggregation for PoC 4.7."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .utils import ensure_dir, timestamp


def _parse_timestamp(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    return value if "_" in value else None


def _find_run_root(path: Path) -> Path:
    current = path.resolve()
    for parent in [current, *current.parents]:
        if (parent / "phase0A_runs").exists():
            return parent
        if parent.name == "phase0A_runs":
            return parent.parent
    return current


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_summary_fallback(run_root: Path) -> Optional[dict]:
    summary_path = run_root / "summary.json"
    if summary_path.exists():
        try:
            return _load_json(summary_path)
        except json.JSONDecodeError:
            return None
    return None


def _normalize_summary(summary: dict, run_root: Path) -> dict:
    normalized = dict(summary)
    normalized.setdefault("run_root", str(run_root))
    normalized.setdefault("generated_at", timestamp())
    normalized.setdefault("latest_manifests", {})
    normalized.setdefault("mismatch_forks", [])
    normalized.setdefault("spec_map_check", None)
    normalized.setdefault("manifests", [])
    if "phases_present" not in normalized:
        phases = sorted((normalized.get("latest_manifests") or {}).keys())
        normalized["phases_present"] = phases
    return normalized


def _collect_manifests(run_root: Path) -> list[dict]:
    manifests: list[dict] = []
    for manifest_path in run_root.rglob("run_manifest.json"):
        try:
            data = _load_json(manifest_path)
        except json.JSONDecodeError:
            continue
        data["_path"] = str(manifest_path)
        data["_phase"] = data.get("phase", "unknown")
        manifests.append(data)
    return manifests


def _select_latest(manifests: list[dict]) -> Optional[dict]:
    if not manifests:
        return None
    def sort_key(item: dict) -> str:
        ts = _parse_timestamp(item.get("generated_at"))
        return ts or ""
    return sorted(manifests, key=sort_key, reverse=True)[0]


def build_summary(run_root: Path) -> dict[str, object]:
    manifests = _collect_manifests(run_root)
    if not manifests:
        fallback = _load_summary_fallback(run_root)
        if fallback:
            return _normalize_summary(fallback, run_root)
        raise FileNotFoundError(f"No run_manifest.json files found under {run_root}")

    phases: dict[str, list[dict]] = {}
    for entry in manifests:
        phases.setdefault(str(entry.get("_phase")), []).append(entry)

    latest_by_phase = {phase: _select_latest(items) for phase, items in phases.items()}
    phase0 = latest_by_phase.get("0A")
    phase1a = latest_by_phase.get("1A")
    phase2a = latest_by_phase.get("2A")
    phase2b = latest_by_phase.get("2B")

    spec_map_check = None
    if phase1a and phase1a.get("spec_map_check"):
        spec_map_path = Path(phase1a["spec_map_check"])
        if spec_map_path.exists():
            spec_map_check = _load_json(spec_map_path)

    summary: dict[str, object] = {
        "run_root": str(run_root),
        "generated_at": timestamp(),
        "phases_present": sorted(phases.keys()),
        "latest_manifests": {k: v.get("_path") for k, v in latest_by_phase.items() if v},
        "eip_number": (phase0 or {}).get("eip_number"),
        "fork_name": (phase1a or {}).get("fork_name"),
        "client_name": (phase2a or phase2b or {}).get("client_name"),
        "spec_branch": (phase0 or {}).get("spec_branch"),
        "spec_commit": (phase0 or {}).get("spec_commit"),
        "mismatch_forks": (phase0 or {}).get("mismatch_forks", []),
        "spec_map_check": spec_map_check,
        "manifests": [
            {"phase": m.get("_phase"), "path": m.get("_path")}
            for m in sorted(manifests, key=lambda x: x.get("_path", ""))
        ],
    }
    return summary


def write_report(
    run_root: Path,
    output_dir: Optional[str],
    formats: Optional[list[str]],
) -> Path:
    root = _find_run_root(run_root)
    out_dir = Path(output_dir).expanduser().resolve() if output_dir else root
    ensure_dir(out_dir)

    summary = build_summary(root)
    formats = formats or ["json", "md"]

    if "json" in formats:
        (out_dir / "summary.json").write_text(
            json.dumps(summary, indent=2), encoding="utf-8"
        )

    if "md" in formats:
        lines = [
            "# PoC 4.7 Run Summary",
            "",
            f"- Run root: {summary.get('run_root')}",
            f"- Generated at: {summary.get('generated_at')}",
            f"- EIP: {summary.get('eip_number')}",
            f"- Fork: {summary.get('fork_name')}",
            f"- Client: {summary.get('client_name')}",
            f"- Spec branch: {summary.get('spec_branch')}",
            f"- Spec commit: {summary.get('spec_commit')}",
            "",
            "## Phases",
        ]
        for phase in summary.get("phases_present", []):
            lines.append(f"- {phase}: {summary['latest_manifests'].get(phase)}")
        lines.append("")
        mismatches = summary.get("mismatch_forks", [])
        lines.append(f"## Spec Map Mismatches: {len(mismatches)}")
        if mismatches:
            lines.extend([f"- {fork}" for fork in mismatches])
        else:
            lines.append("- None")
        lines.append("")
        if summary.get("spec_map_check"):
            lines.append("## Spec Map Check (Phase 1A)")
            lines.append("```json")
            lines.append(json.dumps(summary["spec_map_check"], indent=2))
            lines.append("```")
        (out_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")

    return out_dir
