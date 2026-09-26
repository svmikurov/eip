# =============================================================================
# Examples Make commands
# =============================================================================

# Socket commands
# ===============

run-example-socket-echo-server:
	poetry run python3 src/eip/examples/socket/echo_server.py

run-example-socket-echo-client:
	poetry run python3 src/eip/examples/socket/echo_client.py

run-example-socket-multiconn-server:  ## Run socket multi-connect server example with args
	poetry run python3 src/eip/examples/socket/multiconn_server.py 127.0.0.1 65432

run-example-socket-multiconn-client:  ## Run socket multi-connect client example with args
	poetry run python3 src/eip/examples/socket/multiconn_client.py 127.0.0.1 65432 2


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
	@echo ""
	@echo "run-example-socket-echo-server		Run socket echo server example"
	@echo "run-example-socket-echo-client		Run socket echo client example"
	@echo ""
	@echo "run-example-socket-multiconn-server	Run socket multi-connect server example with args"
	@echo "run-example-socket-multiconn-client 	Run socket multi-connect client example with args"
	@echo ""