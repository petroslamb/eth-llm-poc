import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from src.eip_verify.cli import CLI

# Minimal EIP-1559 for testing
DUMMY_EIP_CONTENT = """---
eip: 1559
title: Fee market change for ETH 1.0 chain
status: Final
---

# Abstract

A transaction pricing mechanism.
"""

# Minimal README with the table spec_index.py expects
DUMMY_SPEC_README = """# Execution Specs

### Ethereum Protocol Releases

| | Fork | EIPs |
| - | - | - |
| 1 | London | [EIP-1559](./EIPs/eip-1559.md) |
"""

@pytest.fixture
def mock_environment(tmp_path):
    """Sets up a mock environment with spec repo and client repo."""
    # 1. Setup Spec Repo
    spec_repo = tmp_path / "spec_repo"
    spec_repo.mkdir()
    
    # Create EIPs directory and file
    eips_dir = spec_repo / "EIPs"
    eips_dir.mkdir()
    (eips_dir / "eip-1559.md").write_text(DUMMY_EIP_CONTENT, encoding="utf-8")
    
    # Create README
    (spec_repo / "README.md").write_text(DUMMY_SPEC_README, encoding="utf-8")
    
    # Create fork directory (required by resolver)
    fork_dir = spec_repo / "src" / "ethereum" / "forks" / "london"
    fork_dir.mkdir(parents=True)
    (fork_dir / "__init__.py").touch()

    # 2. Setup Client Repo
    client_repo = tmp_path / "client_repo"
    client_repo.mkdir()
    (client_repo / "go.mod").touch() # Simulate repo root

    # 3. Setup output directory (to ensure we don't pollute CWD)
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()

    return {
        "spec_repo": spec_repo,
        "client_repo": client_repo,
        "output_dir": runs_dir,
    }

def test_pipeline_end_to_end(mock_environment):
    """
    Test the full pipeline execution in fake mode.
    
    Verifies that:
    1. The pipeline runs without error.
    2. All expected phases run.
    3. Artifacts are generated in the specified output directory.
    """
    spec_repo = mock_environment["spec_repo"]
    client_repo = mock_environment["client_repo"]
    output_dir = mock_environment["output_dir"]
    
    cli = CLI()
    
    # We need to run inside the mocks to ensure relative paths work if used,
    # but here we pass absolute paths which determines behavior.
    # However, 'extract' phase might write to CWD if not careful, 
    # but we pass output_dir to pipeline.
    
    phases = "extract,locate-spec,analyze-spec,locate-client,analyze-client"
    
    print(f"Running pipeline test with output_dir: {output_dir}")
    
    # Execute pipeline
    # We use 'fake' mode so no actual LLM calls are made.
    cli.pipeline(
        eip="1559",
        phases=phases,
        spec_repo=str(spec_repo),
        client_repo=str(client_repo),
        output_dir=str(output_dir),
        llm_mode="fake",
        # Use defaults for others or explicit None
    )
    
    # --- Assertions ---

    # 1. check run directory creation
    # The pipeline creates a timestamped folder inside output_dir
    # But wait, our CLI passes output_dir directly. 
    # Let's check how pipeline.py handles it.
    # line 108: run_root = Path(output_dir) if output_dir else ...
    # So it uses output_dir explicitly if provided.
    
    run_root = output_dir
    assert run_root.exists()
    
    # 2. Check summary report
    summary_file = run_root / "summary.md"
    assert summary_file.exists(), "summary.md should be generated"
    content = summary_file.read_text(encoding="utf-8")
    assert "EIP-1559" in content
    
    # 3. Check phase subdirectories
    # Note: runner creates `phaseXA_runs/<timestamp>/...` inside run_root
    
    # Check Phase 0A (Extract)
    phase0_dirs = list((run_root / "phase0A_runs").glob("*"))
    assert len(phase0_dirs) == 1, "Should have exactly one phase0A run"
    assert (phase0_dirs[0] / "obligations_index.csv").exists()
    
    # Check Phase 1A (Locate Spec)
    phase1a_dirs = list(run_root.glob("**/phase1A_runs/*"))
    # Note: nested structure is `parent_run / phase1A_runs / timestamp`.
    # Since we chain them, they will be nested deep.
    # Actually, pipeline.py logic:
    # Phase 0A output is `run_root / phase0A_runs / timestamp`
    # Phase 1A output is `phase0A_output / phase1A_runs / timestamp`
    # etc.
    
    # Let's just verify that deep nesting happened by traversing
    
    # 0A
    p0 = phase0_dirs[0]
    
    # 1A
    p1a_dirs = list((p0 / "phase1A_runs").glob("*"))
    assert len(p1a_dirs) == 1, "Should have phase1A run nested in phase0A"
    p1a = p1a_dirs[0]
    
    # 1B
    p1b_dirs = list((p1a / "phase1B_runs").glob("*"))
    assert len(p1b_dirs) == 1, "Should have phase1B run nested in phase1A"
    p1b = p1b_dirs[0]
    
    # 2A
    p2a_dirs = list((p1b / "phase2A_runs").glob("*"))
    assert len(p2a_dirs) == 1, "Should have phase2A run nested in phase1B"
    p2a = p2a_dirs[0]
    
    # 2B
    p2b_dirs = list((p2a / "phase2B_runs").glob("*"))
    assert len(p2b_dirs) == 1, "Should have phase2B run nested in phase2A"
    p2b = p2b_dirs[0]
    
    print("Verification complete: All phases executed and artifacts found.")
