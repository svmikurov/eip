"""Использование селектора для построения неблокирующего сервера."""

import selectors
import socket
from selectors import SelectorKey
from typing import cast

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8000))
server_socket.listen()

selector = selectors.DefaultSelector()
selector.register(server_socket, selectors.EVENT_READ)

while True:
    events: list[tuple[SelectorKey, int]] = selector.select(timeout=1)

    if len(events) == 0:
        print('Событий нет, подожду еще!')
        continue

    for event, _ in events:
        event_socket = cast(socket.socket, event.fileobj)

        if event_socket == server_socket:
            connection, client_address = event_socket.accept()
            connection.setblocking(False)
            print(f'Получен запрос на подключение от {client_address}')
            selector.register(connection, selectors.EVENT_READ)
        else:
            data = event_socket.recv(1024)
            print(f'Получены данные: {data!r}')
            event_socket.sendall(data)
