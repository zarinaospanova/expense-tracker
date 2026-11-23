"""Tests for the two mitigations (risk register R1 and R2)."""
import json

import pytest

from expense_tracker import cli
from expense_tracker.calculator import parse_amount
from expense_tracker.models import Expense
from expense_tracker.storage import StorageError, load, save


# --- Mitigation 1 (R1): amount input is never executed as code ---

def test_code_in_amount_is_rejected_and_not_executed(tmp_path):
    marker = tmp_path / "pwned.txt"
    payload = f"open({str(marker)!r}, 'w').write('x')"
    with pytest.raises(ValueError):
        parse_amount(payload)
    assert not marker.exists()


def test_simple_sum_still_works():
    assert parse_amount("1500+300") == 1800.0


@pytest.mark.parametrize("bad", ["-500", "0", "1e309", "nan", "abc", ""])
def test_invalid_amounts_are_rejected(bad):
    with pytest.raises(ValueError):
        parse_amount(bad)


# --- Mitigation 2 (R2): first run and damaged data file ---

def test_load_missing_file_returns_empty_list(tmp_path):
    assert load(tmp_path / "missing.json") == []


def test_damaged_file_raises_clear_error_and_is_not_changed(tmp_path):
    path = tmp_path / "expenses.json"
    path.write_text('[{"title": "a", "amount": 1', encoding="utf-8")
    with pytest.raises(StorageError):
        load(path)
    assert path.read_text(encoding="utf-8") == '[{"title": "a", "amount": 1'


def test_round_trip_keeps_all_fields(tmp_path):
    path = tmp_path / "data.json"
    original = [Expense("Book", 10.5, "study", "USD")]
    save(original, path)
    assert load(path) == original
    json.loads(path.read_text(encoding="utf-8"))  # valid JSON


def test_cli_first_run_does_not_crash(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["list"]) == 0
    assert cli.main(["add", "Coffee", "1500", "food"]) == 0
    assert cli.main(["summary"]) == 0
    assert "Total (KZT): 1500.0" in capsys.readouterr().out


def test_cli_rejects_bad_amount_without_saving(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["add", "Hack", "__import__('os')", "food"]) == 2
    assert not (tmp_path / "expenses.json").exists()
