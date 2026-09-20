"""Simple HTTP socket server."""

import random
import socket

HOST, PORT = '0.0.0.0', 8000
HEADERS_END = b'\r\n\r\n'
LISTEN_BACKLOG = 5  # max pending connections in the kernel accept queue
CONNECTION_TIMEOUT = 5.0


def create_socket() -> socket.socket:
    """Create socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(LISTEN_BACKLOG)
    return sock


def read_request(conn: socket.socket) -> bytes | None:
    """Read HTTP request headers from `conn` until the blank line.

    Returns the raw request bytes, or `None` if the peer closed the
    connection before the end of headers was received.
    """
    data = b''
    while HEADERS_END not in data:
        chunk = conn.recv(4096)
        if not chunk:
            return None
        data += chunk
    return data


def make_body() -> bytes:
    """Return a plain-text body with a random number."""
    number = random.randint(1, 1000)
    result = f'Случайное число: {number}\n'.encode('utf-8')
    return result


def create_response(body: bytes) -> bytes:
    """Create response."""
    return (
        b'HTTP/1.1 200 OK\r\n'
        b'Content-Type: text/plain; charset=utf-8\r\n'
        b'Content-Length: ' + str(len(body)).encode() + b'\r\n'
        b'Connection: close\r\n'
        b'\r\n' + body
    )


def handle_client(conn: socket.socket) -> None:
    """Handle client request."""
    try:
        data = read_request(conn)
        if data is None:
            return
        body = make_body()
        response = create_response(body)
        conn.sendall(response)

    except TimeoutError:
        print(f'Client timed out: {conn.getpeername()}')

    finally:
        conn.close()


def main() -> None:
    """Run server."""
    sock = create_socket()

    try:
        while True:
            conn, addr = sock.accept()

            print(f'Connection from {addr[0]}:{addr[1]}')

            conn.settimeout(CONNECTION_TIMEOUT)
            handle_client(conn)

    except KeyboardInterrupt:
        print('\nShutting down...')

    finally:
        sock.close()


if __name__ == '__main__':
    main()
