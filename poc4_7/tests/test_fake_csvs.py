from pathlib import Path

from poc4_7.fake_agent import _write_fake_client_csv, _write_fake_obligations_csv


def test_write_fake_obligations_csv(tmp_path: Path) -> None:
    output = tmp_path / "obligations.csv"

    _write_fake_obligations_csv(output, "7702")

    text = output.read_text(encoding="utf-8")
    assert "EIP7702-OBL-001" in text
    assert "fake" in text


def test_write_fake_client_csv(tmp_path: Path) -> None:
    input_csv = tmp_path / "input.csv"
    output_csv = tmp_path / "output.csv"

    input_csv.write_text(
        "id,category,enforcement_type,statement,locations,code_flow,obligation_gap,code_gap\n"
        "EIP7702-OBL-001,fake,,Fake obligation,,,,\n",
        encoding="utf-8",
    )

    _write_fake_client_csv(input_csv, output_csv)

    text = output_csv.read_text(encoding="utf-8")
    assert "client_locations" in text
    assert "client_code_flow" in text
