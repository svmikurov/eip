# =============================================================================
# Infrastructure layer development Make commands
# =============================================================================

# Socket commands
# ~~~~~~~~~~~~~~~

run-socket-server:  ## Run socket server example
	poetry run python3 src/eip/infrastructure/endpoints/server.py

run-socket-client:  ## Run socket client example
	poetry run python3 src/eip/infrastructure/endpoints/client.py

run-socket-multiconn_server:  ## Run socket multi-connect server example
	poetry run python3 src/eip/infrastructure/endpoints/multiconn_server.py 127.0.0.1 65432

run-socket-multiconn_client:  ## Run socket multi-connect client example
	poetry run python3 src/eip/infrastructure/endpoints/multiconn_client.py 127.0.0.1 65432 2

help-infra:
	@echo "=============================================="
	@echo "Infrastructure layer development Make commands"
	@echo "=============================================="
	@echo ""
	@echo "Socket commands"
	@echo "~~~~~~~~~~~~~~~"
	@echo "run-socket-server		Run socket server example"
	@echo "run-socket-client		Run socket client example"
	@echo "run-socket-multiconn_server	Run socket multi-connect server example"
	@echo "run-socket-multiconn_client	Run socket multi-connect client example"