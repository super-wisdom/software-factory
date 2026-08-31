import datetime

import pytest

from software_factory import cli

TRACKER_STUB = """# Delivery Tracker

## In flight

| ID | Feature / fix | Worktree / stream | Intent | Spec | Plan | Build | Test | Review | Deploy | Owner | Notes |
|----|---------------|-------------------|:------:|:----:|:----:|:-----:|:----:|:------:|:------:|:-----:|-------|

_Nothing in flight._

## Shipped (archive)

| ID | Feature / fix | Shipped date | PR | Eval added? | Notes |
|----|---------------|:------------:|----|:-----------:|-------|
"""


def make_repo(tmp_path, with_tracker=False):
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
    if with_tracker:
        (tmp_path / "DELIVERY-TRACKER.md").write_text(TRACKER_STUB)
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


def test_new_refuses_to_overwrite(tmp_path, monkeypatch):
    r = make_repo(tmp_path)
    monkeypatch.chdir(r)
    cli.main(["new", "First"])
    with pytest.raises(SystemExit):
        cli.main(["new", "Dup", "--id", "F-001"])
    assert "First" in (r / "intent" / "F-001.md").read_text()


def test_invalid_id_rejected(tmp_path, monkeypatch):
    r = make_repo(tmp_path)
    monkeypatch.chdir(r)
    with pytest.raises(SystemExit):
        cli.main(["new", "Bad", "--id", "XYZ"])


def test_new_appends_inflight_row_and_clears_placeholder(tmp_path, monkeypatch, capsys):
    r = make_repo(tmp_path, with_tracker=True)
    monkeypatch.chdir(r)
    assert cli.main(["new", "Export to CSV"]) == 0
    tracker = (r / "DELIVERY-TRACKER.md").read_text()
    assert "| F-001 | Export to CSV | feat/F-001-export-to-csv |" in tracker
    assert "_Nothing in flight._" not in tracker  # placeholder removed
    assert "updated DELIVERY-TRACKER.md" in capsys.readouterr().out


def test_new_tracker_is_idempotent(tmp_path, monkeypatch):
    r = make_repo(tmp_path, with_tracker=True)
    monkeypatch.chdir(r)
    cli.main(["new", "One"])
    # a second unit lands as its own row; the first stays exactly once
    cli.main(["new", "Two"])
    tracker = (r / "DELIVERY-TRACKER.md").read_text()
    assert tracker.count("| F-001 |") == 1
    assert tracker.count("| F-002 |") == 1


def test_new_no_tracker_flag_skips(tmp_path, monkeypatch, capsys):
    r = make_repo(tmp_path, with_tracker=True)
    monkeypatch.chdir(r)
    cli.main(["new", "Skip", "--no-tracker"])
    tracker = (r / "DELIVERY-TRACKER.md").read_text()
    assert "| F-001 |" not in tracker
    assert "paste into DELIVERY-TRACKER.md" in capsys.readouterr().out


def test_new_without_tracker_file_is_graceful(tmp_path, monkeypatch, capsys):
    r = make_repo(tmp_path, with_tracker=False)
    monkeypatch.chdir(r)
    assert cli.main(["new", "No tracker here"]) == 0
    assert "paste into DELIVERY-TRACKER.md" in capsys.readouterr().out
