import csv
from pathlib import Path

from poc4_7.runner import write_stub_client_csv, write_stub_obligations_csv


def test_write_stub_obligations_csv(tmp_path: Path) -> None:
    output = tmp_path / "obligations_index.csv"
    write_stub_obligations_csv(output, "7702")

    with output.open(encoding="utf-8", newline="") as handle:
        header = handle.readline().strip()

    assert (
        header
        == "id,category,enforcement_type,statement,locations,code_flow,obligation_gap,code_gap"
    )

    with output.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    assert len(rows) == 1
    assert rows[0]["id"] == "EIP7702-OBL-001"


def test_write_stub_client_csv(tmp_path: Path) -> None:
    input_csv = tmp_path / "input.csv"
    with input_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "id",
                "category",
                "enforcement_type",
                "statement",
                "locations",
                "code_flow",
                "obligation_gap",
                "code_gap",
            ]
        )
        writer.writerow([
            "EIP7702-OBL-001",
            "stub",
            "",
            "Stub obligation",
            "",
            "",
            "",
            "",
        ])

    output_csv = tmp_path / "output.csv"
    write_stub_client_csv(input_csv, output_csv)

    with output_csv.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    assert len(rows) == 1
    assert "client_locations" in reader.fieldnames
    assert "client_code_flow" in reader.fieldnames
    assert "client_obligation_gap" in reader.fieldnames
    assert "client_code_gap" in reader.fieldnames
