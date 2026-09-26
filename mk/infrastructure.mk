# =============================================================================
# Infrastructure layer Make commands
# =============================================================================

# Socket commands
# ===============

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
	@echo "build-socket-http-server	Build HTTP socket server Docker image"
	@echo "run-socket-http-server		Run HTTP socket server Docker container on: 127.0.0.1:8001"
	@echo "stop-socket-http-server		Stop HTTP socket server Docker container"
	@echo ""