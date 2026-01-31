"""Run report aggregation for PoC 4.7."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Optional, Any

from .utils import ensure_dir, timestamp

PHASE_DESCRIPTIONS = {
    "0A": "Obligation extraction + indexing",
    "1A": "Per-obligation implementation locations",
    "1B": "Code flow + gap hints per obligation",
    "2A": "Client implementation locations",
    "2B": "Client gap analysis",
}

CONFIG_KEYS = [
    "model",
    "max_turns",
    "llm_mode",
    "record_llm_calls",
    "allowed_tools",
    "obligation_id",
]


def phase_label(phase: str) -> str:
    description = PHASE_DESCRIPTIONS.get(phase)
    return f"{phase} — {description}" if description else phase


def _merge_run_config(latest_by_phase: dict[str, Optional[dict]]) -> dict[str, object]:
    merged: dict[str, object] = {}
    for phase in ["0A", "1A", "1B", "2A", "2B"]:
        manifest = latest_by_phase.get(phase) or {}
        for key in CONFIG_KEYS:
            if key not in merged and key in manifest:
                merged[key] = manifest.get(key)
    return merged


def _parse_timestamp(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    return value if "_" in value else None


def _ascii_bar(count: int, total: int, width: int = 10) -> str:
    if total == 0:
        return "[" + " " * width + "] 0%"
    fraction = count / total
    filled = int(fraction * width)
    bar = "█" * filled + "░" * (width - filled)
    percent = int(fraction * 100)
    return f"[{bar}] {percent}%"


def _analyze_csv(csv_path: Path) -> dict[str, Any]:
    if not csv_path.exists():
        return {}
    
    rows: list[dict] = []
    try:
        with csv_path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception:
        return {"error": "Failed to parse CSV"}

    total_rows = len(rows)
    if total_rows == 0:
        return {"total_rows": 0}

    stats = {}
    fieldnames = list(rows[0].keys()) if rows else []
    
    for field in fieldnames:
        populated = sum(1 for r in rows if r.get(field, "").strip())
        stats[field] = {
            "populated": populated,
            "total": total_rows,
            "percent": int((populated / total_rows) * 100) if total_rows > 0 else 0,
            "ascii_bar": _ascii_bar(populated, total_rows),
        }

    findings = {}
    gap_columns = ["obligation_gap", "code_gap", "client_obligation_gap", "client_code_gap"]
    for col in gap_columns:
        if col not in fieldnames:
            continue
        
        column_findings = []
        for row in rows:
            val = row.get(col, "").strip()
            if val:
                column_findings.append({
                    "id": row.get("id", "unknown"),
                    "text": val
                })
        findings[col] = column_findings

    return {
        "source_csv": str(csv_path),
        "total_rows": total_rows,
        "stats": stats,
        "findings": findings,
    }


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
    run_config = _merge_run_config(latest_by_phase)

    spec_map_check = None
    if phase1a and phase1a.get("spec_map_check"):
        spec_map_path = Path(phase1a["spec_map_check"])
        if spec_map_path.exists():
            spec_map_check = _load_json(spec_map_path)

    # Find the best CSV for analysis
    # Preference: Phase 2B -> 2A -> 1B -> 1A -> 0A
    analysis_csv: Optional[str] = None
    analysis_phase: Optional[str] = None
    
    for phase in ["2B", "2A", "1B", "1A", "0A"]:
        manifest = latest_by_phase.get(phase)
        if manifest and manifest.get("output_csv"):
             path = Path(manifest["output_csv"])
             if path.exists():
                 analysis_csv = str(path)
                 analysis_phase = phase
                 break
    
    csv_analysis = _analyze_csv(Path(analysis_csv)) if analysis_csv else None

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
        "run_config": run_config,
        "csv_analysis": csv_analysis,
        "analysis_phase": analysis_phase,
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
        def format_value(value: object) -> str:
            if value is None:
                return "None"
            if isinstance(value, list):
                return ", ".join(str(item) for item in value) if value else "None"
            return str(value)

        run_config = summary.get("run_config", {}) or {}
        lines = [
            "# PoC 4.7 Run Summary",
            "",
            "## Run configuration",
            f"- Run root: {summary.get('run_root')}",
            f"- Generated at: {summary.get('generated_at')}",
            f"- EIP: {format_value(summary.get('eip_number'))}",
            f"- Fork: {format_value(summary.get('fork_name'))}",
            f"- Client: {format_value(summary.get('client_name'))}",
            f"- Spec branch: {format_value(summary.get('spec_branch'))}",
            f"- Spec commit: {format_value(summary.get('spec_commit'))}",
            f"- Model: {format_value(run_config.get('model'))}",
            f"- Max turns: {format_value(run_config.get('max_turns'))}",
            f"- LLM mode: {format_value(run_config.get('llm_mode'))}",
            f"- Record LLM calls: {format_value(run_config.get('record_llm_calls'))}",
            f"- Allowed tools: {format_value(run_config.get('allowed_tools'))}",
            f"- Obligation filter: {format_value(run_config.get('obligation_id'))}",
            "",
            "## Phases",
        ]
        for phase in summary.get("phases_present", []):
            lines.append(
                f"- {phase_label(phase)}: {summary['latest_manifests'].get(phase)}"
            )
        lines.append("")
        mismatches = summary.get("mismatch_forks", [])
        lines.append("## Spec Map Mismatches")
        lines.append(
            "These are forks where execution-specs README EIP lists disagree with "
            "fork __init__ EIP lists (captured in Phase 0A)."
        )
        lines.append(f"- Count: {len(mismatches)}")
        if mismatches:
            lines.extend([f"- {fork}" for fork in mismatches])
        else:
            lines.append("- None")
        lines.append("")
        if summary.get("spec_map_check"):
            lines.append("## Spec Map Check (Phase 1A)")
            lines.append(
                "Phase 1A validates the selected fork against the Phase 0A EIP→fork map "
                "and reports whether the README and fork __init__ agree."
            )
            lines.append(
                "Status meanings: ok, mismatch, fork_not_found, invalid_json, missing."
            )
            lines.append("```json")
            lines.append(json.dumps(summary["spec_map_check"], indent=2))
            lines.append("```")
        
        analysis = summary.get("csv_analysis")
        phase_label_str = summary.get("analysis_phase") or "Unknown"
        
        if analysis and analysis.get("total_rows", 0) > 0:
            lines.append("")
            lines.append(f"## Statistics (Phase {phase_label_str})")
            lines.append(f"- Source: `{analysis.get('source_csv')}`")
            lines.append(f"- Total Obligations: **{analysis['total_rows']}**")
            lines.append("")
            lines.append("| Column | Populated | % | Progress |")
            lines.append("|---|---|---|---|")
            
            stats = analysis.get("stats", {})
            for field, data in stats.items():
                lines.append(f"| {field} | {data['populated']} | {data['percent']}% | `{data['ascii_bar']}` |")
            
            lines.append("")
            lines.append("## Findings")
            
            findings = analysis.get("findings", {})
            has_findings = False
            for category, items in findings.items():
                if not items:
                    continue
                has_findings = True
                lines.append(f"### {category}")
                
                # Grouping logic: if > 20, show top 20 and count
                limit = 20
                displayed = items[:limit]
                
                for item in displayed:
                    lines.append(f"- **{item['id']}**: {item['text']}")
                
                if len(items) > limit:
                    lines.append(f"- ... and {len(items) - limit} more.")
                lines.append("")
            
            if not has_findings:
                lines.append("- No gaps found in analyzed columns.")

        # Append Full CSV Raw Content (with size guard)
        if analysis and analysis.get("source_csv"):
            csv_path = Path(analysis["source_csv"])
            if csv_path.exists():
                raw_content = csv_path.read_text(encoding="utf-8")
                # 500KB limit for GitHub Step Summary (1MB max total)
                MAX_SIZE = 500 * 1024 
                if len(raw_content) > MAX_SIZE:
                    raw_content = raw_content[:MAX_SIZE] + "\n... (Truncated due to size limit)"
                
                lines.append("")
                lines.append("<details>")
                lines.append(f"<summary>Full CSV Output (Phase {phase_label_str})</summary>")
                lines.append("")
                lines.append("```csv")
                lines.append(raw_content)
                lines.append("```")
                lines.append("</details>")

        (out_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")

    return out_dir
