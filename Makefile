.RECIPEPREFIX := >
.PHONY: install test lint build check

install:
> python -m pip install -U pip
> pip install -e ".[dev]"

test:
> pytest -q

lint:
> ruff check .
> ruff format --check .

build:
> python -m compileall -q src

check: lint test build
> @echo "== all checks passed =="
