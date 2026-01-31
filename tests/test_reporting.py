import csv
import json
from pathlib import Path
import pytest
from eip_verify.reporting import build_summary, write_report, _ascii_bar

def test_ascii_bar():
    assert _ascii_bar(0, 100) == "[░░░░░░░░░░] 0%"
    assert _ascii_bar(50, 100) == "[█████░░░░░] 50%"
    assert _ascii_bar(100, 100) == "[██████████] 100%"
    assert _ascii_bar(0, 0) == "[          ] 0%"

@pytest.fixture
def fake_run_dir(tmp_path):
    """Create a fake run directory structure"""
    # Create phases structure
    phase0 = tmp_path / "phase0A_runs" / "20230101_100000"
    phase1a = phase0 / "phase1A_runs" / "20230101_101000"
    phase1b = phase1a / "phase1B_runs" / "20230101_102000"
    phase2a = phase1b / "phase2A_runs" / "20230101_103000"
    phase2b = phase2a / "phase2B_runs" / "20230101_104000"
    
    phase2b.mkdir(parents=True)
    
    # Create phase 2B manifest
    manifest2b = {
        "phase": "2B",
        "generated_at": "20230101_104000",
        "output_csv": str(phase2b / "client_obligations_index.csv"),
    }
    (phase2b / "run_manifest.json").write_text(json.dumps(manifest2b))
    
    return phase2b

def test_build_summary_stats(fake_run_dir):
    """Test that statistics are calculated correctly from the CSV"""
    csv_path = fake_run_dir / "client_obligations_index.csv"
    
    fieldnames = [
        "id", "locations", "obligation_gap", "code_gap",
        "client_obligation_gap", "client_code_gap"
    ]
    
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # Row 1: Full
        writer.writerow({
            "id": "1", "locations": "loc", "obligation_gap": "", 
            "code_gap": "", "client_obligation_gap": "", "client_code_gap": ""
        })
        # Row 2: Gaps
        writer.writerow({
            "id": "2", "locations": "", "obligation_gap": "Gap1", 
            "code_gap": "Codegap1", "client_obligation_gap": "Clientgap1", "client_code_gap": ""
        })
        # Row 3: Empty
        writer.writerow({
            "id": "3", "locations": "", "obligation_gap": "", 
            "code_gap": "", "client_obligation_gap": "", "client_code_gap": ""
        })

    # Run from the root of the run (which is what write_report does internally typically)
    # But build_summary expects the run_root to contain manifests.
    # Our fake_run_dir is the leaf Phase 2B dir.
    # build_summary logic: _collect_manifests scans rglob("run_manifest.json")
    
    summary = build_summary(fake_run_dir)
    
    analysis = summary.get("csv_analysis")
    assert analysis is not None
    assert analysis["total_rows"] == 3
    
    # Check Stats
    stats = analysis["stats"]
    assert stats["id"]["populated"] == 3
    assert stats["locations"]["populated"] == 1
    assert stats["locations"]["percent"] == 33
    
    # Check Findings
    findings = analysis["findings"]
    assert len(findings["obligation_gap"]) == 1
    assert findings["obligation_gap"][0]["text"] == "Gap1"
    assert len(findings["client_obligation_gap"]) == 1
    assert findings["client_obligation_gap"][0]["text"] == "Clientgap1"
    assert len(findings["client_code_gap"]) == 0

def test_write_report_markdown(fake_run_dir):
    """Test markdown report generation"""
    # Create minimal valid CSV
    csv_path = fake_run_dir / "client_obligations_index.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "obligation_gap"])
        writer.writeheader()
        writer.writerow({"id": "1", "obligation_gap": "Serious Gap"})

    output_dir = write_report(fake_run_dir, output_dir=None, formats=["md"])
    report_path = output_dir / "summary.md"
    
    assert report_path.exists()
    content = report_path.read_text()
    
    assert "## Statistics (Phase 2B)" in content
    assert "Total Obligations: **1**" in content
    assert "Serious Gap" in content
    assert "## Findings" in content
    
    # Check Definitions
    assert "## Definitions" in content
    assert "obligation_gap" in content
    assert "discrepancies between the extracted obligation" in content.lower()
    
    # Check Dropdown
    assert "<details>" in content
    assert "Full CSV Output" in content
    assert "id,obligation_gap" in content  # CSV header
    assert "1,Serious Gap" in content      # CSV row
