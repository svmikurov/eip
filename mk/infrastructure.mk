# =============================================================================
# Infrastructure layer Make commands
# =============================================================================

# Socket commands
# ===============

run-socket-server:  ## Run socket server example
	poetry run python3 src/eip/infrastructure/endpoints/server.py

run-socket-client:  ## Run socket client example
	poetry run python3 src/eip/infrastructure/endpoints/client.py

run-socket-multiconn-server:  ## Run socket multi-connect server example with args
	poetry run python3 src/eip/infrastructure/endpoints/multiconn_server.py 127.0.0.1 65432

run-socket-multiconn-client:  ## Run socket multi-connect client example with args
	poetry run python3 src/eip/infrastructure/endpoints/multiconn_client.py 127.0.0.1 65432 2

run-socket-app-server:  # Run application socket server with args
	poetry run python3 src/eip/infrastructure/endpoints/app_server.py '' 65432

run-socket-app-client:  # Run application socket client with args
	poetry run python3 src/eip/infrastructure/endpoints/app_client.py 127.0.0.1 65432 binary 😃

# Docker http socket server commands
# ----------------------------------

build-socket-http-server:  # Build HTTP socket server Docker image
	docker build -f docker/infrastructure/socket/Dockerfile -t socket-http-server .

run-socket-http-server:  # Run HTTP socket server Docker container on: 127.0.0.1:8001
	docker run -d --rm --name socket-http-server -p 8001:8000 socket-http-server

stop-socket-http-server:  # Stop HTTP socket server Docker container
	docker stop socket-http-server

# Help
# ====

help-infra:
	@echo ""
	@echo "=================================================================="
	@echo "Infrastructure layer Make commands"
	@echo "=================================================================="
	@echo ""
	@echo "Socket commands"
	@echo "==============="
	@echo "run-socket-server		Run socket server example"
	@echo "run-socket-client		Run socket client example"
	@echo "run-socket-multiconn-server	Run socket multi-connect server example (with args)"
	@echo "run-socket-multiconn-client	Run socket multi-connect client example (with args)"
	@echo "run-socket-app-server		Run application socket server (with args)"
	@echo "run-socket-app-client		Run application socket client (with args)"
	@echo ""
	@echo "build-socket-http-server	Build HTTP socket server Docker image"
	@echo "run-socket-http-server		Run HTTP socket server Docker container on: 127.0.0.1:8001"
	@echo "stop-socket-http-server		Stop HTTP socket server Docker container"
	@echo ""