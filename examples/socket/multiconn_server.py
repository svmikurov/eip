"""Multi-connection socket server example."""

import selectors
import socket
import sys
from dataclasses import dataclass
from typing import TypeAlias, cast

EventMaskT: TypeAlias = int
EventsT: TypeAlias = list[tuple[selectors.SelectorKey, EventMaskT]]

MAX_MESSAGE_LEN = 1024

sel = selectors.DefaultSelector()


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


def add_listening_socket() -> None:
    """Create listening socket and register it."""
    host, port = get_args()

    lsock = build_socket()
    lsock.bind((host, port))
    lsock.setblocking(False)

    lsock.listen()
    print(f'Listening on ({host, port})')

    sel.register(lsock, selectors.EVENT_READ, data=None)


def accept_wrapper(lsock: socket.socket) -> None:
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


def service_connection(key: selectors.SelectorKey, mask: int) -> None:
    """Service connection."""
    conn = cast(socket.socket, key.fileobj)
    data: ServerData = key.data

    if mask & selectors.EVENT_READ:
        recv_data = conn.recv(
            MAX_MESSAGE_LEN
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
    add_listening_socket()

    try:
        events: EventsT = sel.select(timeout=None)

        for key, mask in events:
            if key.data is None:
                lsock = cast(socket.socket, key.fileobj)
                accept_wrapper(lsock)
            else:
                service_connection(key, mask)

    except KeyboardInterrupt:
        print('Caught keyboard interrupt, exiting')

    finally:
        sel.close()


if __name__ == '__main__':
    main()
