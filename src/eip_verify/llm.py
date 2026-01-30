"""LLM configuration and call recording helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable, Optional

from .utils import timestamp


DEFAULT_ALLOWED_TOOLS = ["Read", "Write", "Bash", "Grep", "Glob"]


@dataclass(frozen=True)
class ClaudeConfig:
    model: Optional[str]
    max_turns: int
    allowed_tools: list[str]
    llm_mode: str = "live"
    record_calls: bool = False


def build_claude_config(
    model: Optional[str],
    max_turns: int,
    allowed_tools: Optional[Iterable[str]],
    llm_mode: str = "live",
    record_calls: bool = False,
) -> ClaudeConfig:
    tools = list(allowed_tools) if allowed_tools else DEFAULT_ALLOWED_TOOLS
    return ClaudeConfig(
        model=model,
        max_turns=max_turns,
        allowed_tools=tools,
        llm_mode=llm_mode,
        record_calls=record_calls,
    )


def config_metadata(config: ClaudeConfig) -> dict[str, object]:
    return {
        "model": config.model,
        "max_turns": config.max_turns,
        "allowed_tools": list(config.allowed_tools),
        "llm_mode": config.llm_mode,
        "record_llm_calls": config.record_calls,
    }


def write_llm_call_record(
    *,
    output_path: Path,
    prompt: str,
    options_kwargs: dict[str, object],
    config: ClaudeConfig,
    used_fake: bool,
) -> Path:
    record_path = output_path.with_suffix(".call.json")
    record = {
        "recorded_at": timestamp(),
        "llm_mode": config.llm_mode,
        "used_fake": used_fake,
        "prompt": prompt,
        "options": options_kwargs,
        "output_path": str(output_path),
    }
    record_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record_path
