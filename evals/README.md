# Evals -- agent-config regression suite

Treat CLAUDE.md, skills, hooks, and templates like code: when you change them, prove you
did not break an invariant the agent (or the `factory` tool) relies on.

## Run
```bash
factory eval                      # all tasks must pass
factory eval --min-pass-rate 0.8  # allow a threshold
```
Or in CI: `python -m software_factory.cli eval` (see .github/workflows/agent-evals.yml).

## Add a task
Drop a JSON object (or a list of them) into `evals/tasks/*.json`:
```json
{ "id": "unique-id",
  "description": "what invariant this protects",
  "cmd": "grep -q 'something' SOME_FILE",
  "expect_exit": 0,
  "expect_contains": "optional stdout/stderr substring" }
```
Each `cmd` runs from the repo root. Keep tasks deterministic and dependency-free.
Start small: a handful that guard your riskiest config beats fifty that guard nothing.
