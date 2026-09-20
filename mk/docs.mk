# =============================================================================
# Documentation Make commands
# =============================================================================

# Environment commands
# ====================

docs-build:  # Build documentation
	poetry run make -C docs html

# Help
# ====

help-docs:
	@echo ""
	@echo "=================================================================="
	@echo "Documentation Make commands"
	@echo "=================================================================="
	@echo ""
	@echo "Environment commands"
	@echo "===================="
	@echo "docs-build		Build documentation"
	@echo ""