"""Multi-connection socket server example.

Ключевое:
- select() следит за всеми сокетами сразу.
- Один поток обслуживает много соединений.
- Новые клиенты принимаются, не блокируя остальных.
"""

import selectors
import socket
import sys
from dataclasses import dataclass
from typing import TypeAlias, cast

from eip.examples.socket import conf

EventMaskT: TypeAlias = int
EventsT: TypeAlias = list[tuple[selectors.SelectorKey, EventMaskT]]


@dataclass
class ServerData:
    """Server connection data."""

    addr: tuple[str, int]
    inb: bytes = b''
    outb: bytes = b''


def get_args() -> tuple[str, int]:
    """Get args of server run command."""
    host, port = sys.argv[1], int(sys.argv[2])
    return host, port


def build_socket() -> socket.socket:
    """Build listen socket."""
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return lsock


def create_listening_socket() -> socket.socket:
    """Create listening socket and register it."""
    host, port = get_args()

    lsock = build_socket()
    lsock.bind((host, port))
    lsock.setblocking(False)

    lsock.listen()
    print(f'Listening on {host, port}')

    return lsock


def accept_wrapper(
    lsock: socket.socket, sel: selectors.DefaultSelector
) -> None:
    """Accept the incoming connection and register it."""
    conn, addr = lsock.accept()
    print(f'Accepted connection from {addr}')

    # Configure the connection socket in non-blocking mode
    conn.setblocking(False)

    data = ServerData(addr=addr)
    # send() может заблокироваться, если буфер отправки полон.
    # Чтобы не блокировать цикл — ждём EVENT_WRITE
    events = selectors.EVENT_READ | selectors.EVENT_WRITE

    sel.register(conn, events, data=data)


def service_connection(
    key: selectors.SelectorKey, mask: int, sel: selectors.DefaultSelector
) -> None:
    """Service connection."""
    conn = cast(socket.socket, key.fileobj)
    data: ServerData = key.data

    if mask & selectors.EVENT_READ:
        recv_data = conn.recv(
            conf.MAX_MESSAGE_LEN
        )  # Connection should be ready to read

        if recv_data:
            # Echo server sends received data
            data.outb += recv_data
        else:
            print(f'Closing connection to {data.addr}')
            sel.unregister(conn)
            conn.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f'Echoing {data.outb!r} to {data.addr}')
            # send() returns sent bytes count
            sent = conn.send(data.outb)  # Connection should be ready to write
            data.outb = data.outb[sent:]


def main() -> None:
    """Run server."""
    listen_sock = create_listening_socket()
    sel = selectors.DefaultSelector()
    sel.register(listen_sock, selectors.EVENT_READ, data=None)

    try:
        while True:
            # Block until there are sockets ready for I/O.
            events: EventsT = sel.select(timeout=None)

            for key, mask in events:
                # New client have no socket data.
                # Socket data will be set on connection accept.

                if key.data is None:
                    # New client connection handling
                    registered_sock = cast(socket.socket, key.fileobj)
                    accept_wrapper(registered_sock, sel)

                else:
                    # Existing client connection handling
                    service_connection(key, mask, sel)

    except KeyboardInterrupt:
        print('\nCaught keyboard interrupt, exiting')

    except Exception as exc:
        print(f'Got unexpected {exc}')

    finally:
        sel.close()


if __name__ == '__main__':
    main()
