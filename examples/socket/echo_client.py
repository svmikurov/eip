"""Socket echo client."""

import socket

# Server address
HOST = '127.0.0.1'
PORT = 8080
ADDR = (HOST, PORT)

# Socket configuration
MAX_MESSAGE_LEN = 1024


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(ADDR)

    sock.sendall(b'Hello, word!')

    data = sock.recv(MAX_MESSAGE_LEN)

print(f'Received {data!r}')
