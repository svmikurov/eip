# =============================================================================
# Code quality Make commands
# =============================================================================


# Linter commands
# ==============

lint: # Check code style (read-only)
	poetry run ruff check

fix:  # Auto-fix lint issues
	poetry run ruff check --fix

format:  # Format code with ruff
	poetry run ruff format


# Type check commands
# ===================

type-check:  # Check types with mypy
	poetry run mypy .


# Run tests commands
# ==================

test:  # Run tests
	poetry run pytest -v


# Combined check commands
# =======================

ci: lint type-check test  # CI check (read-only: lint + type-check + test)

check: format fix type-check test  # Full check (format + fix + type-check + test)


# Help
# ====

help-code-quality:
	@echo ""
	@echo "=================================================================="
	@echo "Code quality Make commands"
	@echo "=================================================================="
	@echo ""
	@echo "Linter commands"
	@echo "==============="
	@echo "lint				Check code style (read-only)"
	@echo "fix				Auto-fix lint issues"
	@echo "format				Format code with ruff"
	@echo ""
	@echo "Type check commands"
	@echo "==================="
	@echo "type-check			Check types with mypy"
	@echo ""
	@echo "Run test commands"
	@echo "================="
	@echo "test				Run tests"
	@echo ""
	@echo ""
	@echo "Combined check commands"
	@echo "======================="
	@echo "ci				CI check (read-only: lint + type-check + test)"
	@echo "check				Full check (format + fix + type-check + test)"
	@echo ""
