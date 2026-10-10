"""Асинхронный контекстный менеджер, ожидающий подключения клиента."""

import asyncio
import socket
from types import TracebackType
from typing import Type


class ConnectedSocket:
    """Connected socket."""

    def __init__(
        self,
        server_socket: socket.socket,
    ) -> None:
        self._server_socket = server_socket
        self._connection: socket.socket | None = None

    async def __aenter__(self) -> socket.socket:
        print('Вход в контекстный менеджер, ожидающий подключение')

        loop = asyncio.get_event_loop()
        connection, address = await loop.sock_accept(self._server_socket)

        print(f'Подключение с адресом {address} подтверждено')
        self._connection = connection
        return self._connection

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        if self._connection:
            print('Выход из контекстного менеджера, закрытие подключения')
            self._connection.close()
            print('Подключение закрыто')


async def main() -> None:
    """Run server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    socket_addres = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(socket_addres)
    server_socket.listen()

    loop = asyncio.get_event_loop()

    async with ConnectedSocket(server_socket) as connection:
        data = await loop.sock_recv(connection, 1024)
        print(f'Получены данные {data!r}')


if __name__ == '__main__':
    asyncio.run(main())
