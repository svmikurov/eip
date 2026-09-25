"""Multi-connection socket client."""

import selectors
import socket
from dataclasses import dataclass
from typing import cast
from . import conf

IO_EVENTS = selectors.EVENT_READ | selectors.EVENT_WRITE

sel = selectors.DefaultSelector()
messages = [b'Message 1 from client.', b'Message 2 from client.']


@dataclass
class ClientData:
    """Client connection data."""

    conn_id: int
    msg_total: int
    recv_total: int = 0
    messages: list[bytes] = []
    outb: bytes = b''


def start_connection(host: str, port: int, num_conns: int) -> None:
    """Start connection."""
    for conn_id in range(1, num_conns + 1):
        print(f'Starting connection {conn_id} to {(host, port)}')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex((host, port))

        data = ClientData(
            conn_id=conn_id,
            msg_total=sum(len(message) for message in messages),
            messages=messages.copy(),
        )

        sel.register(sock, IO_EVENTS, data=data)


def service_connection(key: selectors.SelectorKey, mask: int) -> None:
    """Service connection."""
    conn = cast(socket.socket, key.fileobj)
    data: ClientData = key.data

    if mask & selectors.EVENT_READ:
        recv_data: bytes = conn.recv(conf.MAX_MESSAGE_LEN)

        if recv_data:
            print(f'Received {recv_data!r} from connection {data.conn_id}')
            data.recv_total += len(recv_data)

        if not recv_data or data.recv_total == data.msg_total:
            print(f'Closing connection {data.conn_id}')
            sel.unregister(conn)
            conn.close()

    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)

        if data.outb:
            print(f'Sending {data.outb!r} to {data.conn_id}')
            sent = conn.send(data.outb)
            data.outb = data.outb[sent:]
