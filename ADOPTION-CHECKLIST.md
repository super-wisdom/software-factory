# Software Factory — Adoption Checklist

Concrete setup tasks, in dependency order. Each item is verifiable (you can tell when it's
truly done). Check off as you go; mirror status in `ADOPTION-TRACKER.md`.

Rule of thumb: **don't start a phase until the previous phase's "done when" is true.**

---

## Phase 0 — Factory floor (target: a few days)
*Done when: a fresh Claude Code session reads your `CLAUDE.md` and can run all checks with one command each.*

- [ ] Create/confirm the repo and the folder layout from `FACTORY-DESIGN.md`.
- [ ] Run `/init` in the repo to generate a starting `CLAUDE.md`.
- [ ] Cut `CLAUDE.md` to **one page**: build/test/lint commands, key conventions, "things Claude gets wrong". Commit it.
- [ ] Wrap checks into single commands that exit non-zero on failure: `make test`, `make build`, `make lint` (or `npm` equivalents).
- [ ] Add a "Verifying your work" block to `CLAUDE.md` (run all three, paste output, fix code not tests).
- [ ] Create empty `intent/`, `specs/`, `plans/` folders (add a `.gitkeep`).
- [ ] Verify: open a new session, ask Claude to run the checks — it should succeed unassisted.

## Phase 1 — Artifact chain (target: 1–2 weeks)
*Done when: your last 3 changes each have a committed intent → spec → plan before any code.*

- [ ] Copy the templates in `templates/` (`intent.md`, `spec.md`, `plan.md`) into your flow.
- [ ] Ship your **first** real feature through the full chain by hand:
  - [ ] Brainstorm with Claude → commit `intent/<feature>.md`.
  - [ ] Generate + review → commit `specs/<feature>.md`.
  - [ ] Start Claude Code in **plan mode**, feed it the spec, interrogate it → commit `plans/<feature>.md`.
  - [ ] Accept the plan, let it implement, confirm tests green, open PR.
- [ ] Add `DELIVERY-TRACKER.md` and log that feature as your first tracked unit.
- [ ] Make plan mode your **default** session start for anything non-trivial.

## Phase 2 — Standards + guardrails (target: 1–2 weeks)
*Done when: at least one policy is enforced by a skill, and one must-hold rule is enforced by a hook.*

- [ ] List the 1–3 things you enforce inconsistently today (e.g. an API convention, a security rule).
- [ ] Write the top one as a skill: `.claude/skills/<name>/SKILL.md` (frontmatter = when it triggers; body = what to do).
- [ ] Test the skill triggers: ask for the task 3 different ways, confirm it loads each time.
- [ ] Add a minimal `.claude/settings.json` with build-time hooks: block edits to protected paths, run formatter after edits, keep secrets out of the diff.
- [ ] Add one **subagent**: `.claude/agents/verifier.md` (runs the app, checks behavior, reports only).
- [ ] Adopt the working rule: **a mistake seen twice → correction goes into `CLAUDE.md` or a skill.**

## Phase 3 — Automated review + CI (target: ~2 weeks)
*Done when: every PR gets an automatic review and your eval suite runs on config changes + nightly.*

- [ ] Turn on AI PR review (managed Code Review service, or `claude-code-action` in GitHub Actions).
- [ ] Write `REVIEW.md`: define Important vs nit, cap nits, list paths to skip.
- [ ] Enable branch protection: require a human (you) to approve before merge.
- [ ] Wire `@claude` on PR comments so the agent addresses review notes and pushes fixes.
- [ ] Build an eval suite: collect 20–50 real recent tasks with pass/fail checks in `evals/`.
- [ ] Add `.github/workflows/agent-evals.yml` — runs on changes to `CLAUDE.md`/`.claude/**` and on a nightly cron.
- [ ] Gate config changes on eval pass rate (a skill change that drops the rate gets reviewed).

## Phase 4 — Close the loop (defer until you have live traffic)
*Done when: a monitored metric breach writes an `intent.md` into your triage queue with no human in the path.*

- [ ] Pick one metric with a stable baseline (e.g. post-deploy 5xx rate, CI failure rate).
- [ ] Write a **deterministic** detection script (rolling mean/stddev, version-controlled, unit-tested).
- [ ] Define response tiers in `bands.yaml` (log at 1σ, read-only diagnose at 2σ, propose-PR at 3σ).
- [ ] Prove and rehearse a one-command **rollback** path in staging.
- [ ] On each shipped fix, add an eval for the incident so it can't regress.
- [ ] (Optional) Add Claude Tag in Slack so incidents/tickets can enter the loop from chat.

---

### What you are deliberately NOT doing (skip list)
- MDM/managed enterprise settings, separation-of-duties across people, change boards.
- Requirements tools with regulatory traceability, dual source-of-truth reconciliation.
- Per-environment deployment tiering across many environments.
Revisit only if you take on regulated work or grow the team.
