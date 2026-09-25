"""Socket echo server."""

import socket

from eip.examples.socket import conf

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(conf.ADDR)
    sock.listen(conf.BACKLOG)

    conn, addr = sock.accept()

    with conn:
        print(f'Connected by {addr}')

        while True:
            data = conn.recv(conf.MAX_MESSAGE_LEN)
            if not data:
                break

            conn.sendall(data)
