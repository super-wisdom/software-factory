# Evals — agent-config regression suite

Purpose: treat `CLAUDE.md`, skills, and hooks like code. When you change them, prove you
didn't regress the agent's behaviour.

## Shape
- Put 20–50 real, recent tasks in `evals/tasks/` — each with a clear pass/fail check
  (an expected file change, a command that must exit 0, a string that must appear).
- Wire a runner in `.github/workflows/agent-evals.yml` to execute them and report a pass rate.
- A config change that drops the pass rate gets reviewed before it merges.

Start small: 5 tasks that cover your riskiest workflows beats 50 that cover nothing.
