import json
from pathlib import Path

from poc4_7.runner import DEFAULT_ALLOWED_TOOLS, build_claude_config, run_query


def test_stub_mode_records_call_and_output(tmp_path: Path) -> None:
    repo_root = tmp_path
    output_path = tmp_path / "phase_output.txt"
    stub_response = tmp_path / "stub_response.txt"
    stub_response.write_text("stubbed output\n", encoding="utf-8")

    config = build_claude_config(
        model="claude-sonnet-4-5",
        max_turns=1,
        allowed_tools=None,
        llm_mode="stub",
        record_calls=True,
        stub_response_path=str(stub_response),
    )

    run_query("hello stub", output_path, repo_root, config)

    assert output_path.read_text(encoding="utf-8") == "stubbed output\n"

    call_path = output_path.with_suffix(".call.json")
    assert call_path.exists()

    record = json.loads(call_path.read_text(encoding="utf-8"))
    assert record["llm_mode"] == "stub"
    assert record["used_stub"] is True
    assert record["prompt"] == "hello stub"
    assert record["options"]["max_turns"] == 1
    assert record["options"]["cwd"] == str(repo_root)
    assert record["options"]["model"] == "claude-sonnet-4-5"
    assert record["options"]["allowed_tools"] == DEFAULT_ALLOWED_TOOLS
    assert record["output_path"] == str(output_path)
