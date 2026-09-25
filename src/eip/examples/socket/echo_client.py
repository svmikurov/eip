"""Socket echo client."""

import socket

from eip.examples.socket import conf

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(conf.ADDR)

    sock.sendall(b'Hello, word!')

    data = sock.recv(conf.MAX_MESSAGE_LEN)

print(f'Received {data!r}')
