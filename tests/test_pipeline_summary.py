import os
from pathlib import Path
from unittest.mock import patch
from eip_verify.pipeline import _log_phase_to_summary

def test_log_phase_to_summary(tmp_path):
    """Test that phase artifacts are correctly appended to the summary."""
    # Setup mock run dir with artifacts
    run_dir = tmp_path / "run_dir"
    run_dir.mkdir()
    (run_dir / "phase_prompt.txt").write_text("Prompt content")
    (run_dir / "phase_output.txt").write_text("Output content")
    
    # Setup mock summary file
    summary_file = tmp_path / "summary.md"
    summary_file.touch()
    
    # Mock environment variable
    with patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": str(summary_file)}):
        _log_phase_to_summary("extract", run_dir)
        
    content = summary_file.read_text()
    
    assert "<details>" in content
    assert "<summary>Phase extract Artifacts</summary>" in content
    assert "#### phase_prompt.txt" in content
    assert "Prompt content" in content
    assert "#### phase_output.txt" in content
    assert "Output content" in content

def test_log_phase_no_artifacts(tmp_path):
    """Test that nothing is logged if no artifacts exist."""
    run_dir = tmp_path / "empty_run_dir"
    run_dir.mkdir()
    
    summary_file = tmp_path / "summary.md"
    summary_file.touch()
    
    with patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": str(summary_file)}):
        _log_phase_to_summary("extract", run_dir)
        
    content = summary_file.read_text()
    assert content == ""

def test_truncation(tmp_path):
    """Test that large artifacts are truncated."""
    run_dir = tmp_path / "large_run_dir"
    run_dir.mkdir()
    
    # create > 20KB file (much larger to ensure truncation is obvious despite wrapper overhead)
    large_content = "A" * (20 * 1024 + 10000)
    (run_dir / "large_prompt.txt").write_text(large_content)
    
    summary_file = tmp_path / "summary.md"
    summary_file.touch()
    
    with patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": str(summary_file)}):
        _log_phase_to_summary("extract", run_dir)
        
    content = summary_file.read_text()
    assert "... (Truncated)" in content
    # Now valid because we removed 10000 chars and added only ~150 chars of wrapper
    assert len(content) < len(large_content)
