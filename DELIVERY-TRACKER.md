# Delivery Tracker — The Production Line

This is the **recurring** tracker: every feature/fix in flight and where it is on the line.
This is the engine of predictable delivery. Update it as units move; commit changes so the
git history is your delivery audit trail.

**WIP limit: 2–3 units in the Build column at once** (one per parallel worktree). Adding a
4th only makes sense if review is still keeping up — the throttle is *your* review capacity,
not the model's speed.

**Stage legend (each cell = the artifact/gate for that stage):**
`⬜ not yet` · `🟡 in progress` · `✅ committed/passed`

- **Intent** = `intent/<id>.md` accepted
- **Spec** = `specs/<id>.md` accepted
- **Plan** = `plans/<id>.md` accepted (plan mode)
- **Build** = implemented, feedback loop green
- **Test** = tests/build/lint green, pasted in PR
- **Review** = AI review clean + human approved
- **Deploy** = merged & shipped

---

## In flight

| ID | Feature / fix | Worktree / stream | Intent | Spec | Plan | Build | Test | Review | Deploy | Owner | Notes / blockers |
|----|---------------|-------------------|:------:|:----:|:----:|:-----:|:----:|:------:|:------:|:-----:|------------------|
| F-001 | _example: claims status self-service_ | feat-claims-status | ✅ | ✅ | ✅ | 🟡 | ⬜ | ⬜ | ⬜ | ENG | caching for 50rps limit |
| F-002 | | | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | | |
| F-003 | | | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | | |

## Backlog (accepted intents not yet started)

| ID | Feature / fix | Intent committed | Priority | Notes |
|----|---------------|:----------------:|:--------:|-------|
| | | | | |

## Shipped (archive)

| ID | Feature / fix | Shipped date | PR | Eval added? | Notes |
|----|---------------|:------------:|----|:-----------:|-------|
| | | | | | |

---

## How to run a unit through the line

1. **Idea in** → brainstorm with Claude, commit `intent/<id>.md`, add a row here (Backlog).
2. **Pull to In flight** → generate + accept `spec.md`, then plan mode → accept `plan.md`.
3. **Assign a worktree** → `git worktree add ../<id> <branch>`; start a Claude session there.
4. **Build** → let it implement in auto mode; the feedback loop keeps it green. Update Build/Test cells.
5. **PR** → AI review runs; tag `@claude` to address findings; you approve on intent + risk.
6. **Deploy** → merge, ship, move the row to Shipped, and add an eval if it was a bug fix.

## Steering discipline (parallel streams)
- Only run parallel units whose `plan.md` files touch **different files**. Same-file units queue in one session.
- Keep Build-column WIP ≤ your review capacity (start at 2).
- If a stream stalls waiting on your input, that's a signal you're over the WIP limit — finish before starting.
