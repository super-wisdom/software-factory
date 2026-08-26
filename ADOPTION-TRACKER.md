# Software Factory — Adoption Tracker

Tracks the rollout of the factory itself. Update the Status and dates as you go; commit changes
so the git history records when each capability came online. Pair with `ADOPTION-CHECKLIST.md`
(the checklist is the *tasks*; this is the *status roll-up*).

**Status legend:** `⬜ Not started` · `🟡 In progress` · `✅ Done` · `⏸ Deferred`

**Owner:** PO (product owner hat) / ENG (engineer hat) / — (either)

---

## Phase status

| Phase | Capability | Status | Owner | Started | Done | Success metric | Notes |
|------:|------------|:------:|:-----:|---------|------|----------------|-------|
| 0 | Repo layout + folders | ⬜ | ENG | | | Layout matches design | |
| 0 | `CLAUDE.md` (one page) | ⬜ | ENG | | | Fresh session runs checks unassisted | |
| 0 | One-command test/build/lint | ⬜ | ENG | | | `make test/build/lint` exit non-zero on fail | |
| 1 | Artifact templates in use | ⬜ | — | | | intent/spec/plan committed for a real feature | |
| 1 | First feature through full chain | ⬜ | — | | | 1 unit reached PR with all 3 artifacts | |
| 1 | Plan mode = default | ⬜ | ENG | | | Non-trivial work starts in plan mode | |
| 2 | First skill (encoded standard) | ⬜ | ENG | | | Skill triggers on 3/3 phrasings | |
| 2 | Build-time hooks | ⬜ | ENG | | | Protected-path edit is blocked | |
| 2 | `verifier` subagent | ⬜ | ENG | | | Runs app + reports before "done" | |
| 3 | AI PR review on | ⬜ | ENG | | | Every PR gets an auto review | |
| 3 | `REVIEW.md` policy | ⬜ | PO | | | Important vs nit defined; nits capped | |
| 3 | Branch protection | ⬜ | ENG | | | Human approval required to merge | |
| 3 | Eval suite + CI | ⬜ | ENG | | | Evals run on config change + nightly | |
| 4 | Deterministic detection script | ⏸ | ENG | | | Band breach detected reliably | Defer until live traffic |
| 4 | `bands.yaml` tiers | ⏸ | ENG | | | 1σ/2σ/3σ tiers wired | Defer |
| 4 | Rehearsed rollback | ⏸ | ENG | | | Rollback proven in staging | Defer |
| 4 | Loop closes (breach → intent.md) | ⏸ | — | | | intent.md appears with no human | Defer |

---

## Health metrics (fill in as the factory matures)

Read most of these straight from git / PR / CI history.

| Metric | Baseline (before) | Now | Target | Source |
|--------|-------------------|-----|--------|--------|
| Time: first conversation → committed `intent.md` | weeks | | hours | git log on `intent/` |
| Time: `intent.md` → `spec.md` (same change) | | | hours | two git timestamps |
| Share of changes merged on first implementation pass | | | rising | PR metadata |
| Rework cycles per change | | | falling | PR history |
| First-pass CI success rate (agent changes) | | | rising | CI |
| Review time per PR | | | falling | PR metadata |
| Concurrent streams per person (while review holds) | 1 | | 2–3 | your log |
| Changes merged per week | | | rising | PR history |
| Change failure rate | | | falling | incidents |

---

## Decision log

Record dated decisions here (stack picks, policy changes, why a phase was deferred).

| Date | Decision | Rationale |
|------|----------|-----------|
| | | |
