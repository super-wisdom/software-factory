import subprocess
import sys

import pytest

from software_factory import cli


def test_package_name_variants():
    assert cli.package_name("my-new-app") == "my_new_app"
    assert cli.package_name("My Cool API") == "my_cool_api"
    assert cli.package_name("123start").startswith("pkg_")


def test_init_scaffolds_and_substitutes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["init", "my-new-app"]) == 0
    root = tmp_path / "my-new-app"
    assert (root / "CLAUDE.md").exists()
    assert (root / ".claude" / "settings.json").exists()
    assert (root / ".github" / "workflows" / "ci.yml").exists()
    assert (root / "templates" / "intent.md").exists()
    assert (root / "intent" / ".gitkeep").exists()
    # package dir renamed, tokens substituted
    core = (root / "src" / "my_new_app" / "core.py").read_text()
    assert "my-new-app: ok" in core
    assert "__pkg__" not in str(list(root.rglob("*")))
    assert (root / "tests" / "test_smoke.py").read_text().startswith("from my_new_app import")
    # CLAUDE.md carries the project name
    assert "my-new-app" in (root / "CLAUDE.md").read_text()


def test_init_refuses_nonempty_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "taken").mkdir()
    (tmp_path / "taken" / "x").write_text("busy")
    with pytest.raises(SystemExit):
        cli.main(["init", "taken"])


def test_init_generated_project_passes_its_own_checks(tmp_path, monkeypatch):
    """End-to-end: the scaffolded project's own test suite is green."""
    monkeypatch.chdir(tmp_path)
    cli.main(["init", "demo-app"])
    root = tmp_path / "demo-app"
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stdout + r.stderr
