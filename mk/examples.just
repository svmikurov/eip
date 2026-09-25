# =============================================================================
# Examples just commands
# =============================================================================

set working-directory := '..'

# Socket commands
# ===============

# Run socket echo server example
run-socket-echo-server:
    poetry run python3 examples/socket/echo_server.py 127.0.0.1 8080

# Run socket echo client example
run-socket-echo-client:
    poetry run python3 examples/socket/echo_client.py