"""Test socket server."""

import socket


def test_server(server: tuple[str, int]) -> None:
    """Server running."""
    # Arrange
    message = b'Hello word'

    # Act & Assert
    with socket.create_connection(server, timeout=1.0) as sock:
        sock.sendall(message)
        assert sock.recv(1024) == message
