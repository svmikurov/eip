"""Socket clients."""

import socket
from typing import TypeVar

HOST = '127.0.0.1'
PORT = 65432


MessageT = TypeVar('MessageT')


class SocketClient:
    """Socket client."""

    def __init__(
        self,
        host: str,
        port: int,
    ) -> None:
        self._host = host
        self._port = port

    def send(self) -> None:
        """Send message."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b'Hello, world')
            data = s.recv(1024)

        print(f'Received {data!r}')
        print('Connection closed')


def main() -> None:
    """Run client."""
    client = SocketClient(HOST, PORT)
    print('Socket client initialized.')
    client.send()


if __name__ == '__main__':
    main()
