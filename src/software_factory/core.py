"""Seed module so the factory's one-command checks pass on a fresh clone.

Replace this with your real product code. Keep every change covered by a test
in tests/ so `make check` stays green -- that green is the Test station's gate.
"""


def healthcheck() -> str:
    """Return a readiness string used by the smoke test."""
    return "software-factory: ok"
