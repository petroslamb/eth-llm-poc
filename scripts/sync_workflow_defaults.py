#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOLVE_DEFAULTS = ROOT / ".github/workflows/resolve_defaults.yml"
TARGETS = [
    ROOT / ".github/workflows/manual_run.yml",
    ROOT / ".github/workflows/manual_run_batch.yml",
]

DEFAULT_PATTERN = re.compile(
    r'^\s*DEFAULT_([A-Z0-9_]+)=("([^"]*)"|\'([^\']*)\')',
    re.MULTILINE,
)


def parse_defaults(text: str) -> dict[str, str]:
    defaults: dict[str, str] = {}
    for match in DEFAULT_PATTERN.finditer(text):
        key = match.group(1)
        value = match.group(3) if match.group(3) is not None else match.group(4)
        defaults[key] = value
    return defaults


def indent_level(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def quote_value(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', "\\\"")
    return f'"{escaped}"'


def find_input_blocks(lines: list[str]) -> dict[str, tuple[int, int, int]]:
    blocks: dict[str, tuple[int, int, int]] = {}
    dispatch_indent = None
    inputs_indent = None
    in_dispatch = False
    in_inputs = False

    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^\s*workflow_dispatch:\s*$', line):
            dispatch_indent = indent_level(line)
            inputs_indent = None
            in_dispatch = True
            in_inputs = False
            i += 1
            continue

        if in_dispatch:
            if line.strip() and indent_level(line) <= dispatch_indent:
                in_dispatch = False
                in_inputs = False
                inputs_indent = None
            elif re.match(r'^\s*inputs:\s*$', line):
                inputs_indent = indent_level(line)
                in_inputs = True
                i += 1
                continue
            elif in_inputs and line.strip() and indent_level(line) <= inputs_indent:
                in_inputs = False

        if in_inputs and line.strip().endswith(":") and indent_level(line) == inputs_indent + 2:
            name = line.strip()[:-1]
            start = i
            i += 1
            while i < len(lines):
                probe = lines[i]
                if probe.strip() and indent_level(probe) <= inputs_indent:
                    break
                if probe.strip().endswith(":") and indent_level(probe) == inputs_indent + 2:
                    break
                i += 1
            end = i
            blocks[name] = (start, end, inputs_indent + 4)
            continue

        i += 1

    return blocks


def update_workflow_defaults(path: Path, defaults: dict[str, str]) -> bool:
    text = path.read_text()
    lines = text.splitlines()
    blocks = find_input_blocks(lines)

    missing_inputs = [name for name in defaults.keys() if name not in blocks]
    if missing_inputs:
        missing_display = ", ".join(missing_inputs)
        raise RuntimeError(f"Missing inputs in {path}: {missing_display}")

    # Update from bottom to top to avoid index drift on insert.
    ordered_blocks = sorted(
        ((name, blocks[name]) for name in defaults.keys()),
        key=lambda item: item[1][0],
        reverse=True,
    )

    changed = False
    for name, (start, end, prop_indent) in ordered_blocks:
        default_line_idx = None
        type_line_idx = None
        for idx in range(start + 1, end):
            stripped = lines[idx].lstrip(" ")
            if stripped.startswith("default:"):
                default_line_idx = idx
            if stripped.startswith("type:"):
                type_line_idx = idx

        new_default_line = " " * prop_indent + f"default: {quote_value(defaults[name])}"
        if default_line_idx is not None:
            if lines[default_line_idx] != new_default_line:
                lines[default_line_idx] = new_default_line
                changed = True
        else:
            insert_at = type_line_idx + 1 if type_line_idx is not None else end
            lines.insert(insert_at, new_default_line)
            changed = True

    new_text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    if new_text != text:
        path.write_text(new_text)
    return changed


def main() -> int:
    defaults_text = RESOLVE_DEFAULTS.read_text()
    defaults = parse_defaults(defaults_text)

    required = [
        "EIP_SINGLE",
        "EIP_BATCH",
        "FORK",
        "CLIENT",
        "PHASES",
        "MODEL",
        "MAX_TURNS",
        "EIPS_REF",
        "EXECUTION_SPECS_REF",
        "LLM_MODE",
        "PYPI_PACKAGE",
    ]
    for key in required:
        if key not in defaults:
            raise RuntimeError(f"Missing {key} in {RESOLVE_DEFAULTS}")

    default_client = defaults["CLIENT"]
    client_ref_key = f"{default_client.upper()}_REF"
    if client_ref_key not in defaults:
        raise RuntimeError(
            f"Missing {client_ref_key} for default client {default_client} in {RESOLVE_DEFAULTS}"
        )

    shared_defaults = {
        "fork": defaults["FORK"],
        "client": defaults["CLIENT"],
        "client_ref": defaults[client_ref_key],
        "phases": defaults["PHASES"],
        "model": defaults["MODEL"],
        "max_turns": defaults["MAX_TURNS"],
        "eips_ref": defaults["EIPS_REF"],
        "execution_specs_ref": defaults["EXECUTION_SPECS_REF"],
        "llm_mode": defaults["LLM_MODE"],
        "pypi_package": defaults["PYPI_PACKAGE"],
    }

    single_defaults = {"eip": defaults["EIP_SINGLE"], **shared_defaults}
    batch_defaults = {"eip": defaults["EIP_BATCH"], **shared_defaults}

    updated_any = False
    updated_any |= update_workflow_defaults(TARGETS[0], single_defaults)
    updated_any |= update_workflow_defaults(TARGETS[1], batch_defaults)

    if updated_any:
        print("Updated workflow_dispatch defaults from resolve_defaults.yml")
    else:
        print("No workflow defaults changes needed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
