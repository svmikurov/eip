setup:
	poetry install

lint:
	poetry run ruff check

fix:
	poetry run ruff check --fix
	
format:
	poetry run ruff format

type-check:
	poetry run mypy .

test:
	poetry run pytest --cov=src/eip --cov-report=html

check: format fix type-check test

.PHONY: docs
docs:
	poetry run make -C docs clean html