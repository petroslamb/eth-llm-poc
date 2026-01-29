"""Shared utilities for PoC 4.7."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def notes_root(repo_root: Path) -> Path:
    return repo_root / "poc4_7" / "notes" / "generated"
