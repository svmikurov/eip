# =============================================================================
# Examples Make commands
# =============================================================================

# Socket commands
# ===============

run-example-socket-echo-server:
	poetry run python3 src/eip/examples/socket/echo_server.py

run-example-socket-echo-client:
	poetry run python3 src/eip/examples/socket/echo_client.py


# Help
# ====

help-examples:
	@echo ""
	@echo "=================================================================="
	@echo "Examples Make commands"
	@echo "=================================================================="
	@echo ""
	@echo "Socket commands"
	@echo "==============="
	@echo "run-example-socket-echo-server		Run socket echo server example"
	@echo "run-example-socket-echo-client		Run socket echo client example"
	@echo ""