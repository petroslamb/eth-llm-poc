"""Prompt loading utilities for PoC 4.7."""

from __future__ import annotations

from importlib import resources
from typing import Iterable


def list_prompts() -> list[str]:
    """Return available prompt filenames bundled with the package."""
    pkg = resources.files("poc4_7").joinpath("prompts")
    return sorted(
        p.name for p in pkg.iterdir() if p.is_file() and p.name.endswith(".txt")
    )


def load_prompt(name: str) -> str:
    """
    Load a prompt by filename (with or without .txt).

    Example:
        load_prompt("phase0A_obligations")
        load_prompt("phase0A_obligations.txt")
    """
    filename = name if name.endswith(".txt") else f"{name}.txt"
    pkg = resources.files("eip_verify").joinpath("prompts")
    return pkg.joinpath(filename).read_text(encoding="utf-8")
