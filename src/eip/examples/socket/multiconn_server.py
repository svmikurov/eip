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


def accept_wrapper(
    listen_sock: socket.socket, sel: selectors.DefaultSelector
) -> None:
    """Accept the incoming connection and register it."""
    conn_sock, addr = listen_sock.accept()
    print(f'Accepted connection from {addr}')

    # Configure the connection socket in non-blocking mode
    conn_sock.setblocking(False)

    data = ServerData(addr=addr)
    # send() может заблокироваться, если буфер отправки полон.
    # Чтобы не блокировать цикл — ждём EVENT_WRITE
    events = selectors.EVENT_READ | selectors.EVENT_WRITE

    sel.register(conn_sock, events, data=data)


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
    host, port = sys.argv[1], int(sys.argv[2])

    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind((host, port))
    listen_sock.setblocking(False)
    listen_sock.listen()
    print(f'Listening on {host, port}')

    # Listen socket for READ events only.
    selector = selectors.DefaultSelector()
    selector.register(listen_sock, selectors.EVENT_READ, data=None)

    try:
        while True:
            # Block until there are sockets ready for I/O (read/write).
            events: EventsT = selector.select(timeout=None)

            for key, mask in events:
                # New client have no socket data.
                # Socket data will be set on connection accept.

                # Accept the incoming connection and register it.
                if key.data is None:
                    registered_sock = cast(socket.socket, key.fileobj)
                    accept_wrapper(registered_sock, selector)

                # Service registred connection.
                else:
                    service_connection(key, mask, selector)

    except KeyboardInterrupt:
        print('\nCaught keyboard interrupt, exiting')

    except Exception as exc:
        print(f'Got unexpected {exc}')

    finally:
        selector.close()


if __name__ == '__main__':
    main()
