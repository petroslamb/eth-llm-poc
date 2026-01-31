import os
import io
from pathlib import Path
from unittest.mock import patch, MagicMock
from eip_verify.pipeline import _log_phase_to_summary, run_pipeline

# Keep existing unit tests for _log_phase_to_summary as they verify the formatting logic
def test_log_phase_to_summary(tmp_path):
    """Test that phase artifacts are correctly appended to the summary."""
    run_dir = tmp_path / "run_dir"
    run_dir.mkdir()
    (run_dir / "phase_prompt.txt").write_text("Prompt content")
    (run_dir / "phase_output.txt").write_text("Output content")
    
    summary_file = tmp_path / "summary.md"
    summary_file.touch()
    
    with patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": str(summary_file)}):
        _log_phase_to_summary("extract", run_dir)
        
    content = summary_file.read_text()
    assert "<details>" in content
    assert "<summary>Phase extract Artifacts</summary>" in content
    assert "Prompt content" in content

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
    assert len(content) < len(large_content)

# New integration test for the bottom-logging logic
@patch("eip_verify.pipeline.run_phase_0a") # Mock actual runner
@patch("eip_verify.pipeline.write_report") # Mock report writer
def test_pipeline_logs_at_bottom(mock_write_report, mock_phase_0a, tmp_path):
    """Test that artifacts are logged AFTER the summary report."""
    
    # Setup mock env
    summary_file = tmp_path / "gh_step_summary.md"
    summary_file.touch()
    
    # Create a fake run output logic
    def side_effect_phase_0a(**kwargs):
        # Create output dir that pipeline expects
        out_dir = Path(kwargs['output_dir']) / "phase0A_runs" / "fake_timestamp"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "prompt.txt").write_text("MY_ARTIFACT")

    mock_phase_0a.side_effect = side_effect_phase_0a

    # Mock write_report to simulate writing the main summary
    def side_effect_write_report(**kwargs):
        (Path(kwargs['run_root']) / "summary.md").write_text("MAIN_REPORT_HEADER")

    mock_write_report.side_effect = side_effect_write_report

    with patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": str(summary_file)}):
            run_pipeline(
                eip="7702",
                phases=["extract"],
                spec_repo="/tmp",
                client_repo="/tmp", # Actually ignored by mock
                eip_file="/tmp/eip.md", # bypassed validation or mocked? validation check exists.
                output_dir=str(tmp_path / "runs")
            )
    
    content = summary_file.read_text()
    
    # Verify order: MAIN_REPORT must appear BEFORE artifacts
    assert "MAIN_REPORT_HEADER" in content
    assert "MY_ARTIFACT" in content
    
    # Check index positions
    report_idx = content.find("MAIN_REPORT_HEADER")
    artifact_idx = content.find("MY_ARTIFACT")
    
    assert report_idx != -1
    assert artifact_idx != -1
    assert report_idx < artifact_idx, "Report should be written before artifacts"
