setup:
	poetry istall

lint:
	poetry run ruff check

fix:
	poetry run ruff check --fix
	
format:
	poetry run ruff format

test:
	poetry run pytest

check: format fix test
