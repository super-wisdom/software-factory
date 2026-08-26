# CLAUDE.md — Software Factory

One page. This is read at the start of every session. Keep it short and current.

## Commands (the only way to check work)
- `make test`  — run the test suite (pytest)
- `make lint`  — ruff check + format check
- `make build` — byte-compile / package step
- `make check` — all of the above; must be green before any PR

## Stack
- Python >= 3.11, src/ layout, tests in tests/. Deps in pyproject.toml.
- Keep it boring and well-documented. Add a dependency only when it removes real work.

## Conventions
- Every feature/fix flows through the line: intent -> spec -> plan -> diff+tests -> PR.
- Do not write code before an accepted `plans/<id>.md` exists. Use plan mode first.
- Small, reviewable diffs. One logical change per PR.
- Every behaviour change ships with a test. Never weaken a test to make it pass.

## Verifying your work (do this before reporting done)
1. Run `make check`. Paste the output.
2. If it fails, fix the code — not the test.
3. For anything user-visible, have the `verifier` subagent confirm behaviour in a fresh context.

## Things to get right
- Never read or print secrets. `.env*` is off-limits (enforced in .claude/settings.json).
- Never force-push or run destructive shell commands (guarded by a PreToolUse hook).
- When a mistake shows up twice, encode the fix here or in a skill so it can't recur.

## Map
- Process + rationale: FACTORY-DESIGN.md
- Rollout: ADOPTION-CHECKLIST.md / ADOPTION-TRACKER.md
- Work in flight: DELIVERY-TRACKER.md
- Artifact templates: templates/
- Dashboard: index.html
