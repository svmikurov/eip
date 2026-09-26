include mk/setup.mk
include mk/docs.mk
include mk/infrastructure.mk
include mk/code_quality.mk
include mk/examples.mk


help:
	@echo "=================================================================="
	@echo "Makefile commands help"
	@echo "=================================================================="
	@echo ""
	@echo "help-setup			Show only setup commands"
	@echo "help-docs			Show only documentation commands"
	@echo "help-infra			Show only infrastructure commands"
	@echo "help-code-quality		Show only code quality commands"
	@echo "help-examples 			Show only code example commands"
	@echo ""
	@echo "help-all 			Show all commands"
	@echo ""


help-all:
	@$(MAKE) --no-print-directory help-setup
	@$(MAKE) --no-print-directory help-docs
	@$(MAKE) --no-print-directory help-infra
	@$(MAKE) --no-print-directory help-code-quality
	@$(MAKE) --no-print-directory help-examples