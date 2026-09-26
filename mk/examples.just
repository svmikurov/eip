# =============================================================================
# Examples just commands
# =============================================================================

set working-directory := '..'

# Socket commands
# ===============

# Run socket multi-connection server example
run-socket-echo-server:
    poetry run python3 src/eip/examples/socket/multiconn_server.py 127.0.0.1 8080

# Run socket multi-connection client example
run-socket-echo-client:
    poetry run python3 src/eip/examples/socket/multiconn_client.py

# Run asyncio server example
run-asyncio-echo-server host port:
    poetry run python3 src/eip/examples/socket/async_server.py {{host}} {{port}}

# Run asyncio client example
run-asyncio-echo-client:
    poetry run python3 src/eip/examples/socket/async_client.py