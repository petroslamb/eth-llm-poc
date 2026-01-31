"""Fake agent implementation for offline/testing runs."""

from __future__ import annotations

import csv
from pathlib import Path

from .llm import ClaudeConfig, write_llm_call_record


def _write_fake_obligations_csv(path: Path, eip_number: str) -> None:
    fieldnames = [
        "id",
        "category",
        "enforcement_type",
        "statement",
        "locations",
        "code_flow",
        "obligation_gap",
        "code_gap",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        
        # Row 1: Perfect obligation
        writer.writerow(
            {
                "id": f"EIP{eip_number}-OBL-001",
                "category": "core",
                "enforcement_type": "state_change",
                "statement": f"Perfect obligation for EIP-{eip_number}.",
                "locations": "spec.py:100",
                "code_flow": "entry -> verification",
                "obligation_gap": "",
                "code_gap": "",
            }
        )
        
        # Row 2: Obligation with gaps
        writer.writerow(
            {
                "id": f"EIP{eip_number}-OBL-002",
                "category": "edge_case",
                "enforcement_type": "check",
                "statement": f"Gap obligation for EIP-{eip_number}.",
                "locations": "spec.py:200",
                "code_flow": "entry -> check",
                "obligation_gap": "Ambiguous specific condition",
                "code_gap": "Missing assertion in spec",
            }
        )
        
        # Row 3: Empty/Missing obligation
        writer.writerow(
            {
                "id": f"EIP{eip_number}-OBL-003",
                "category": "future",
                "enforcement_type": "",
                "statement": f"Empty obligation for EIP-{eip_number}.",
                "locations": "",
                "code_flow": "",
                "obligation_gap": "",
                "code_gap": "",
            }
        )


def _write_fake_client_csv(input_csv: Path, output_csv: Path, phase: str) -> None:
    with input_csv.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        extras = [
            "client_locations",
            "client_code_flow",
            "client_obligation_gap",
            "client_code_gap",
        ]
        for col in extras:
            if col not in fieldnames:
                fieldnames.append(col)
        rows = []
        for row in reader:
            # Initialize extras
            for col in extras:
                row.setdefault(col, "")
            
            # Logic for Phase 2B gaps
            if phase == "2B":
                row_id = row.get("id", "")
                if "OBL-001" in row_id:
                    row["client_locations"] = "client/file.go:50"
                    row["client_code_flow"] = "HandleMsg -> correct"
                elif "OBL-002" in row_id:
                    row["client_locations"] = "client/file.go:99"
                    row["client_obligation_gap"] = "Client implements older version"
                    row["client_code_gap"] = "Missing bounds check"
            
            # Phase 2A just keeps defaults (empty or copied) for now, 
            # or could mirror logic if we wanted 2A to populate locations too.
            if phase == "2A":
                row_id = row.get("id", "")
                if "OBL-001" in row_id:
                     row["client_locations"] = "client/file.go:50"
                if "OBL-002" in row_id:
                     row["client_locations"] = "client/file.go:99"

            rows.append(row)

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


class FakeClaudeAgent:
    def run(
        self,
        prompt: str,
        output_path: Path,
        cwd: Path,
        config: ClaudeConfig,
        metadata: dict[str, object],
    ) -> None:
        options_kwargs: dict[str, object] = {
            "allowed_tools": config.allowed_tools,
            "permission_mode": "bypassPermissions",
            "max_turns": config.max_turns,
            "cwd": str(cwd),
        }
        if config.model:
            options_kwargs["model"] = config.model

        write_llm_call_record(
            output_path=output_path,
            prompt=prompt,
            options_kwargs=options_kwargs,
            config=config,
            used_fake=True,
        )

        output_text = (
            "FAKE MODE: Claude call skipped.\n"
            f"Recorded call metadata in {output_path.with_suffix('.call.json').name}.\n"
        )
        output_path.write_text(output_text, encoding="utf-8")

        phase = str(metadata.get("phase") or "").upper()
        output_csv = Path(metadata["output_csv"]) if metadata.get("output_csv") else None
        input_csv = Path(metadata["input_csv"]) if metadata.get("input_csv") else None
        eip_number = str(metadata.get("eip_number") or "1559")

        if phase == "0A" and output_csv and not output_csv.exists():
            _write_fake_obligations_csv(output_csv, eip_number)
        if phase == "2A" and output_csv and input_csv and input_csv.exists():
            _write_fake_client_csv(input_csv, output_csv, phase="2A")
        if phase == "2B" and output_csv and input_csv and input_csv.exists():
            _write_fake_client_csv(input_csv, output_csv, phase="2B")
