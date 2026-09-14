"""Socket server."""

import socket

HOST = '127.0.0.1'
PORT = 65432


class SocketServer:
    """Socket server."""

    def __init__(
        self,
        host: str,
        port: int,
    ) -> None:
        self._host = host
        self._port = port

    def run(self) -> None:
        """Run server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._host, self._port))
            s.listen()

            print('Socket server is running')

            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)


def main() -> None:
    """Run server."""
    server = SocketServer(HOST, PORT)
    server.run()


if __name__ == '__main__':
    main()
