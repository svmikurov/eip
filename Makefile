include mk/docs.mk
include mk/infrastructure.mk
include mk/code_quality.mk
include mk/examples.mk

setup:
	poetry install

help:
	@echo "=================================================================="
	@echo "Project intall"
	@echo "=================================================================="
	@echo ""
	@echo "setup				Install project"
	@echo ""
	@$(MAKE) --no-print-directory help-docs
	@$(MAKE) --no-print-directory help-infra
	@$(MAKE) --no-print-directory help-code-quality
	@echo ""
	@echo "=================================================================="
	@echo "Makefile commands help"
	@echo "=================================================================="
	@echo ""
	@echo "help-docs			Show only documentation commands"
	@echo "help-infra			Show only infrastructure commands"
	@echo "help-code-quality		Show only code quality commands"
	@echo ""