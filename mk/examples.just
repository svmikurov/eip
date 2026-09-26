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