import json

from software_factory import evals
from software_factory.cli import main


def write_tasks(root, items):
    (root / "evals" / "tasks").mkdir(parents=True)
    (root / "evals" / "tasks" / "t.json").write_text(json.dumps(items))


def make_repo(tmp_path):
    for d in ("templates", "intent", "specs", "plans"):
        (tmp_path / d).mkdir()
    return tmp_path


def test_load_tasks_reads_a_list(tmp_path):
    write_tasks(tmp_path, [{"id": "a", "cmd": "true"}, {"id": "b", "cmd": "true"}])
    tasks = evals.load_tasks(tmp_path / "evals" / "tasks")
    assert [t.id for t in tasks] == ["a", "b"]


def test_run_task_pass_and_fail(tmp_path):
    ok = evals.run_task(evals.Task(id="ok", description="", cmd="true"), tmp_path)
    bad = evals.run_task(evals.Task(id="bad", description="", cmd="false"), tmp_path)
    assert ok.passed and not bad.passed


def test_run_task_contains(tmp_path):
    t = evals.Task(id="c", description="", cmd="echo hello", expect_contains="hello")
    miss = evals.Task(id="m", description="", cmd="echo hello", expect_contains="nope")
    assert evals.run_task(t, tmp_path).passed
    assert not evals.run_task(miss, tmp_path).passed


def test_run_all_rate(tmp_path):
    write_tasks(tmp_path, [{"id": "a", "cmd": "true"}, {"id": "b", "cmd": "false"}])
    results, rate = evals.run_all(tmp_path)
    assert len(results) == 2
    assert rate == 0.5


def test_cmd_eval_exit_codes(tmp_path, monkeypatch):
    r = make_repo(tmp_path)
    write_tasks(r, [{"id": "a", "cmd": "true"}, {"id": "b", "cmd": "false"}])
    monkeypatch.chdir(r)
    assert main(["eval"]) == 1  # default requires 100%
    assert main(["eval", "--min-pass-rate", "0.5"]) == 0
