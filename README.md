# Software Factory

A repo-native, agent-driven production line for a 1–2 person team. Every stage ends by
committing an artifact the next stage reads: **intent → spec → plan → diff + tests → PR**.
The git history is the audit trail.

## Start here
- **`index.html`** — the operations dashboard (open in any browser).
- **`FACTORY-DESIGN.md`** — how the line works and why.
- **`ADOPTION-CHECKLIST.md`** — phase-by-phase setup.
- **`DELIVERY-TRACKER.md`** — features in flight (the daily engine).

## Develop
```bash
make install   # first time: installs dev deps (pytest, ruff)
make check     # lint + test + build — must be green before a PR
```

## Run a unit through the line
1. Brainstorm with Claude → commit `intent/<id>.md` (see `templates/intent.md`).
2. Generate + accept → `specs/<id>.md`.
3. Plan mode → interrogate → accept `plans/<id>.md`.
4. Assign a worktree, let Claude build, keep `make check` green.
5. Open a PR; AI review + your approval; merge.

## Layout
```
CLAUDE.md              one-page context, read every session
.claude/               settings.json (hooks + permissions), agents/, skills/, commands/
intent/ specs/ plans/  the committed artifact chain
evals/                 agent-config regression suite
src/ tests/            product code + tests
.github/workflows/     ci (make check) + agent-evals
templates/             intent / spec / plan blueprints
```
