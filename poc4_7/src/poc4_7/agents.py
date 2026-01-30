"""Agent adapters for LLM calls."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol

import anyio

from .llm import ClaudeConfig, write_llm_call_record


class AgentProtocol(Protocol):
    def run(
        self,
        prompt: str,
        output_path: Path,
        cwd: Path,
        config: ClaudeConfig,
        metadata: dict[str, object],
    ) -> None:
        """Run an agent call and write outputs."""


class ClaudeAgent:
    def run(
        self,
        prompt: str,
        output_path: Path,
        cwd: Path,
        config: ClaudeConfig,
        metadata: dict[str, object],
    ) -> None:
        anyio.run(self._run_async, prompt, output_path, cwd, config)

    async def _run_async(
        self,
        prompt: str,
        output_path: Path,
        cwd: Path,
        config: ClaudeConfig,
    ) -> None:
        options_kwargs: dict[str, object] = {
            "allowed_tools": config.allowed_tools,
            "permission_mode": "bypassPermissions",
            "max_turns": config.max_turns,
            "cwd": str(cwd),
        }
        if config.model:
            options_kwargs["model"] = config.model

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
                used_fake=False,
            )

        text_chunks: list[str] = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        text_chunks.append(block.text)

        output_path.write_text("".join(text_chunks), encoding="utf-8")
