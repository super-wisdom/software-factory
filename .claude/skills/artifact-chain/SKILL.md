---
name: artifact-chain
description: How to start any new unit of work in this repo. Triggers when the user asks to build a feature, fix a bug, add something, or start new work. Enforces the intent -> spec -> plan chain before any code is written.
---

# Artifact chain

When new work starts (a feature, a fix, an enhancement), do NOT jump to code.

1. **Scaffold** the unit: run `factory new "<short title>"`. It creates the intent, spec,
   and plan files with the next id and prints a delivery-tracker row to paste.
2. Fill **`intent/<id>.md`** first — the problem and constraints, in plain words. Stop for
   the human to accept.
3. Then **`specs/<id>.md`**, including quantifiable acceptance criteria. Stop for acceptance.
4. Then **`plans/<id>.md`** in plan mode: exact files that change, order of work, risks, and
   the tests that prove it. Stop for approval.
5. Only after an accepted plan, implement. Keep `make check` green at every step.

Rules that don't bend: never write code before an accepted plan; never weaken a test to make
it pass; when a mistake recurs, encode the fix in CLAUDE.md or a skill so it can't come back.
