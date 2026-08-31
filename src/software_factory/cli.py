"""factory -- command line for running the software factory line."""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

from .evals import run_all
from .scaffold import FILES as SCAFFOLD_FILES

REPO_ROOT_MARKERS = ("templates", "intent", "specs", "plans")
ARTIFACTS = ("intent", "specs", "plans")
TEMPLATE_FILES = {"intent": "intent.md", "specs": "spec.md", "plans": "plan.md"}
ID_RE = re.compile(r"^F-(\d+)$", re.IGNORECASE)
ID_PREFIX_RE = re.compile(r"^F-(\d+)", re.IGNORECASE)
TRACKER = "DELIVERY-TRACKER.md"
IN_PROGRESS = "\U0001f7e1"  # yellow circle
NOT_YET = "\u2b1c"  # white square


def find_repo_root(start: Path) -> Path:
    """Walk up from *start* to the dir holding templates/ intent/ specs/ plans/."""
    for d in [start, *start.parents]:
        if all((d / m).is_dir() for m in REPO_ROOT_MARKERS):
            return d
    raise SystemExit(
        "error: not inside a software-factory repo "
        "(no templates/intent/specs/plans found above the current directory)."
    )


def next_id(root: Path) -> str:
    """Return the next F-NNN id by scanning the artifact folders."""
    highest = 0
    for sub in ARTIFACTS:
        for f in (root / sub).glob("F-*.md"):
            m = ID_PREFIX_RE.match(f.name)
            if m:
                highest = max(highest, int(m.group(1)))
    return f"F-{highest + 1:03d}"


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s or "untitled"


def fill(template: str, fid: str, title: str, date: str) -> str:
    out = template.replace("F-XXX", fid)
    out = out.replace("<short title>", title).replace("<title>", title)
    out = out.replace("<YYYY-MM-DD>", date)
    return out


def inflight_row(fid: str, title: str, branch: str) -> str:
    """Build the DELIVERY-TRACKER 'In flight' row for a freshly-scaffolded unit."""
    cells = [fid, title, branch, IN_PROGRESS] + [NOT_YET] * 6 + ["", ""]
    return "| " + " | ".join(cells) + " |"


def _is_separator(line: str) -> bool:
    s = line.strip()
    return "|" in s and "-" in s and set(s) <= set("|-: ")


def append_inflight_row(root: Path, fid: str, title: str, branch: str) -> bool:
    """Insert an In-flight row into DELIVERY-TRACKER.md. Returns True if written.

    Idempotent (won't duplicate an existing id) and graceful (returns False if the
    tracker or its 'In flight' table is missing rather than raising).
    """
    p = root / TRACKER
    if not p.is_file():
        return False
    lines = p.read_text().splitlines()

    header = next(
        (i for i, ln in enumerate(lines) if ln.strip().lower().startswith("## in flight")),
        None,
    )
    if header is None:
        return False

    # locate the table separator inside the In flight section
    sep = None
    for i in range(header + 1, len(lines)):
        if lines[i].strip().startswith("## "):
            break
        if _is_separator(lines[i]):
            sep = i
            break
    if sep is None:
        return False

    # section body runs until the next "## " heading (or EOF)
    end = next(
        (i for i in range(sep + 1, len(lines)) if lines[i].strip().startswith("## ")),
        len(lines),
    )
    body = [ln for ln in lines[sep + 1 : end] if "_Nothing in flight" not in ln]

    if any(ln.lstrip().startswith(f"| {fid} ") for ln in body):
        return True  # already tracked; nothing to do

    new_body = [inflight_row(fid, title, branch), *body]
    lines = lines[: sep + 1] + new_body + lines[end:]
    p.write_text("\n".join(lines) + "\n")
    return True


def cmd_new(args: argparse.Namespace) -> int:
    root = find_repo_root(Path.cwd())
    fid = args.id or next_id(root)
    if not ID_RE.match(fid):
        raise SystemExit(f"error: id must look like F-001 (got {fid!r}).")
    fid = fid.upper()
    date = _dt.datetime.now().astimezone().date().isoformat()

    planned: dict[Path, str] = {}
    for sub in ARTIFACTS:
        tpl = root / "templates" / TEMPLATE_FILES[sub]
        if not tpl.is_file():
            raise SystemExit(f"error: missing template {tpl}.")
        dest = root / sub / f"{fid}.md"
        if dest.exists():
            raise SystemExit(
                f"error: {dest.relative_to(root)} already exists; aborting (nothing written)."
            )
        planned[dest] = fill(tpl.read_text(), fid, args.title, date)

    for dest, content in planned.items():
        dest.write_text(content)
        print(f"created {dest.relative_to(root)}")

    branch = f"feat/{fid}-{slugify(args.title)}"
    print()
    if not args.no_tracker and append_inflight_row(root, fid, args.title, branch):
        print(f"updated {TRACKER} (added {fid} to In flight)")
    else:
        print("Delivery-tracker row (paste into DELIVERY-TRACKER.md):")
        print(inflight_row(fid, args.title, branch))
    return 0


def cmd_eval(args: argparse.Namespace) -> int:
    root = find_repo_root(Path.cwd())
    results, rate = run_all(root)
    if not results:
        print("no eval tasks found in evals/tasks/ (nothing to check).")
        return 0
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        print(f"[{mark}] {r.task.id} -- {r.detail}")
    passed = sum(r.passed for r in results)
    print(f"\n{passed}/{len(results)} passed ({rate:.0%})")
    return 0 if rate >= args.min_pass_rate else 1


def package_name(project: str) -> str:
    """Turn a project name into a valid, importable Python package name."""
    pkg = re.sub(r"[^0-9a-z]+", "_", project.lower()).strip("_")
    if not pkg or not (pkg[0].isalpha() or pkg[0] == "_"):
        pkg = f"pkg_{pkg}" if pkg else "app"
    return pkg


def cmd_init(args: argparse.Namespace) -> int:
    name = args.name
    if name == ".":
        target = Path.cwd()
        project = target.name
    else:
        target = Path.cwd() / name
        project = name
    pkg = package_name(project)

    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"error: {target} exists and is not empty; aborting.")

    written = 0
    for rel, content in sorted(SCAFFOLD_FILES.items()):
        dest_rel = rel.replace("__pkg__", pkg)
        body = content.replace("{{PROJECT_NAME}}", project).replace("{{PACKAGE_NAME}}", pkg)
        dest = target / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body)
        written += 1

    print(f"scaffolded {project} ({written} files) into {target}")
    print()
    print("next:")
    print(f"  cd {name}" if name != "." else "  # already here")
    print("  python -m venv .venv && source .venv/bin/activate && make install")
    print("  make check")
    print("  git init && git add -A && git commit -m 'chore: initial factory scaffold'")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="factory", description="Run the software factory line.")
    sub = p.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="scaffold a new work unit (intent/spec/plan).")
    new.add_argument("title", help='short human title, e.g. "Export to CSV".')
    new.add_argument("--id", help="override the auto-incremented id (e.g. F-042).")
    new.add_argument(
        "--no-tracker",
        action="store_true",
        help="don't add the unit to DELIVERY-TRACKER.md; print the row instead.",
    )
    new.set_defaults(func=cmd_new)

    ev = sub.add_parser("eval", help="run the agent-config eval suite.")
    ev.add_argument(
        "--min-pass-rate",
        type=float,
        default=1.0,
        help="minimum pass rate to exit 0 (default 1.0 = all must pass).",
    )
    ev.set_defaults(func=cmd_eval)

    ini = sub.add_parser("init", help="scaffold a new project with the factory line.")
    ini.add_argument("name", help='project name, or "." for the current directory.')
    ini.set_defaults(func=cmd_init)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
