"""factory -- command line for running the software factory line."""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

REPO_ROOT_MARKERS = ("templates", "intent", "specs", "plans")
ARTIFACTS = ("intent", "specs", "plans")
TEMPLATE_FILES = {"intent": "intent.md", "specs": "spec.md", "plans": "plan.md"}
ID_RE = re.compile(r"^F-(\d+)$", re.IGNORECASE)
ID_PREFIX_RE = re.compile(r"^F-(\d+)", re.IGNORECASE)


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


def cmd_new(args: argparse.Namespace) -> int:
    root = find_repo_root(Path.cwd())
    fid = args.id or next_id(root)
    if not ID_RE.match(fid):
        raise SystemExit(f"error: id must look like F-001 (got {fid!r}).")
    fid = fid.upper()
    date = _dt.datetime.now().astimezone().date().isoformat()

    # Resolve + pre-check every target before writing anything (no partial writes).
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

    slug = slugify(args.title)
    print()
    print("Delivery-tracker row (paste into DELIVERY-TRACKER.md):")
    print(
        f"| {fid} | {args.title} | feat/{fid}-{slug} "
        f"| \U0001f7e1 | \u2b1c | \u2b1c | \u2b1c | \u2b1c | \u2b1c | \u2b1c |  |  |"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="factory", description="Run the software factory line.")
    sub = p.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new", help="scaffold a new work unit (intent/spec/plan).")
    new.add_argument("title", help='short human title, e.g. "Export to CSV".')
    new.add_argument("--id", help="override the auto-incremented id (e.g. F-042).")
    new.set_defaults(func=cmd_new)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
