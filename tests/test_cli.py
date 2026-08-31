import datetime

import pytest

from software_factory import cli


def make_repo(tmp_path):
    for d in ("templates", "intent", "specs", "plans"):
        (tmp_path / d).mkdir()
    (tmp_path / "templates" / "intent.md").write_text(
        "# Intent: <short title>\nID: F-XXX\nDate: <YYYY-MM-DD>\n"
    )
    (tmp_path / "templates" / "spec.md").write_text(
        "# Spec: <short title>\nID: F-XXX  Derived from: intent/F-XXX.md\n"
    )
    (tmp_path / "templates" / "plan.md").write_text(
        "# Plan: <short title>\nID: F-XXX  From: specs/F-XXX.md  Date: <YYYY-MM-DD>\n"
    )
    return tmp_path


def test_next_id_starts_at_one(tmp_path):
    assert cli.next_id(make_repo(tmp_path)) == "F-001"


def test_next_id_increments_from_highest(tmp_path):
    r = make_repo(tmp_path)
    (r / "intent" / "F-001.md").write_text("x")
    (r / "specs" / "F-003.md").write_text("x")
    assert cli.next_id(r) == "F-004"


def test_new_creates_all_three_filled(tmp_path, monkeypatch, capsys):
    r = make_repo(tmp_path)
    monkeypatch.chdir(r)
    assert cli.main(["new", "Export to CSV"]) == 0
    intent = (r / "intent" / "F-001.md").read_text()
    assert "Export to CSV" in intent
    assert "F-001" in intent
    today = datetime.datetime.now().astimezone().date().isoformat()
    assert today in intent
    assert (r / "specs" / "F-001.md").exists()
    assert (r / "plans" / "F-001.md").exists()
    assert "intent/F-001.md" in (r / "specs" / "F-001.md").read_text()
    out = capsys.readouterr().out
    assert "F-001" in out and "DELIVERY-TRACKER" in out


def test_new_refuses_to_overwrite(tmp_path, monkeypatch):
    r = make_repo(tmp_path)
    monkeypatch.chdir(r)
    cli.main(["new", "First"])
    with pytest.raises(SystemExit):
        cli.main(["new", "Dup", "--id", "F-001"])
    # the original must be untouched
    assert "First" in (r / "intent" / "F-001.md").read_text()


def test_invalid_id_rejected(tmp_path, monkeypatch):
    r = make_repo(tmp_path)
    monkeypatch.chdir(r)
    with pytest.raises(SystemExit):
        cli.main(["new", "Bad", "--id", "XYZ"])
