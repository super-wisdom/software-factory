"""Eval runner: execute config-invariant tasks and report a pass rate.

Tasks live in evals/tasks/*.json. Each task runs a command from the repo root and
passes if the exit code matches (default 0) and, optionally, stdout/stderr contains
an expected string. This is the regression net for agent config (CLAUDE.md, skills,
hooks, templates) -- the things `make check` does not cover.
"""

from __future__ import annotations

import json
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Task:
    id: str
    description: str
    cmd: str
    expect_exit: int = 0
    expect_contains: str | None = None


@dataclass
class Result:
    task: Task
    passed: bool
    detail: str


def load_tasks(tasks_dir: Path) -> list[Task]:
    tasks: list[Task] = []
    for f in sorted(tasks_dir.glob("*.json")):
        data = json.loads(f.read_text())
        items = data if isinstance(data, list) else [data]
        for d in items:
            tasks.append(
                Task(
                    id=d["id"],
                    description=d.get("description", ""),
                    cmd=d["cmd"],
                    expect_exit=d.get("expect_exit", 0),
                    expect_contains=d.get("expect_contains"),
                )
            )
    return tasks


def run_task(task: Task, cwd: Path) -> Result:
    proc = subprocess.run(
        shlex.split(task.cmd), cwd=cwd, capture_output=True, text=True, check=False
    )
    combined = proc.stdout + proc.stderr
    if proc.returncode != task.expect_exit:
        return Result(task, False, f"exit {proc.returncode} (wanted {task.expect_exit})")
    if task.expect_contains and task.expect_contains not in combined:
        return Result(task, False, f"missing text {task.expect_contains!r}")
    return Result(task, True, "ok")


def run_all(root: Path) -> tuple[list[Result], float]:
    tasks = load_tasks(root / "evals" / "tasks")
    results = [run_task(t, root) for t in tasks]
    passed = sum(r.passed for r in results)
    rate = passed / len(results) if results else 1.0
    return results, rate
