"""Socket echo server."""

import socket

# Server address
HOST = '127.0.0.1'
PORT = 8080
ADDR = (HOST, PORT)

# Socket configuration
BACKLOG = 5
MAX_MESSAGE_LEN = 1024


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(ADDR)
    sock.listen(BACKLOG)

    conn, addr = sock.accept()

    with conn:
        print(f'Connected by {addr}')

        while True:
            data = conn.recv(MAX_MESSAGE_LEN)
            if not data:
                break

            conn.sendall(data)
