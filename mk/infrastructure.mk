# =============================================================================
# Infrastructure layer Make commands
# =============================================================================

# Socket commands
# ===============

run-socket-app-server:  # Run application socket server with args
	poetry run python3 src/eip/infrastructure/endpoints/app_server.py '' 65432

run-socket-app-client:  # Run application socket client with args
	poetry run python3 src/eip/infrastructure/endpoints/app_client.py 127.0.0.1 65432 binary 😃

# Docker http socket server commands
# ----------------------------------

build-socket-http-server:  # Build HTTP socket server Docker image
	docker build -f docker/infrastructure/socket/Dockerfile -t socket-http-server .

run-socket-http-server:  # Run HTTP socket server Docker container on: 127.0.0.1:8001
	docker run --rm --name socket-http-server -p 8001:8000 socket-http-server

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
	@echo ""
	@echo "run-socket-app-server		Run application socket server (with args)"
	@echo "run-socket-app-client		Run application socket client (with args)"
	@echo ""
	@echo "build-socket-http-server	Build HTTP socket server Docker image"
	@echo "run-socket-http-server		Run HTTP socket server Docker container on: 127.0.0.1:8001"
	@echo "stop-socket-http-server		Stop HTTP socket server Docker container"
	@echo ""