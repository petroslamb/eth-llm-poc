import json
from pathlib import Path

from poc4_7.llm import DEFAULT_ALLOWED_TOOLS, build_claude_config
from poc4_7.runner import PhaseContext, run_query
from poc4_7.fake_agent import FakeClaudeAgent


def test_fake_mode_records_call_and_output(tmp_path: Path) -> None:
    repo_root = tmp_path
    output_path = tmp_path / "phase_output.txt"

    config = build_claude_config(
        model="claude-sonnet-4-5",
        max_turns=1,
        allowed_tools=None,
        llm_mode="fake",
        record_calls=True,
    )

    run_query(
        "hello fake",
        output_path,
        repo_root,
        config,
        FakeClaudeAgent(),
        PhaseContext(phase="0A"),
    )

    output_text = output_path.read_text(encoding="utf-8")
    assert "FAKE MODE: Claude call skipped." in output_text

    call_path = output_path.with_suffix(".call.json")
    assert call_path.exists()

    record = json.loads(call_path.read_text(encoding="utf-8"))
    assert record["llm_mode"] == "fake"
    assert record["used_fake"] is True
    assert record["prompt"] == "hello fake"
    assert record["options"]["max_turns"] == 1
    assert record["options"]["cwd"] == str(repo_root)
    assert record["options"]["model"] == "claude-sonnet-4-5"
    assert record["options"]["allowed_tools"] == DEFAULT_ALLOWED_TOOLS
    assert record["output_path"] == str(output_path)
