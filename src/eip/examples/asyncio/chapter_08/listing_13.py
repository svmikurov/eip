"""Чат сервер."""

import asyncio
import logging
from asyncio import StreamReader, StreamWriter

HOST = '127.0.0.1'
PORT = 8888


class ChatServer:
    """Чат сервер."""

    def __init__(self) -> None:
        self._username_to_writer: dict[str, StreamWriter] = {}

    async def start_chat_server(self, host: str, port: int) -> None:
        """Запусти чат-сервер."""
        server = await asyncio.start_server(self._client_connected, host, port)
        async with server:
            print('Сервер запущен')
            await server.serve_forever()

    async def _client_connected(
        self, reader: StreamReader, writer: StreamWriter
    ) -> None:
        """Обработай подключение клиента."""
        print('Обработка запроса клиента на подключение')
        command = await reader.readline()
        print(f'CONNECTED {reader} {writer}')
        command, args = command.split(b' ')

        if command == b'CONNECT':
            username = args.replace(b'\n', b'').decode()
            self._add_user(username, reader, writer)
            await self._on_connect(username, writer)
        else:
            logging.error(
                'Получена недопустимая команда от клиента, отключается.'
            )
            writer.close()
            await writer.wait_closed()

    def _add_user(
        self, username: str, reader: StreamReader, writer: StreamWriter
    ) -> None:
        self._username_to_writer[username] = writer
        print(f'Подключился пользователь: {username}')
        asyncio.create_task(self._listen_for_messages(username, reader))

    async def _on_connect(self, username: str, writer: StreamWriter) -> None:
        writer.write(
            f'Добро пожаловать! Число подключенных пользователей: '
            f'{len(self._username_to_writer)}\n'.encode()
        )
        await writer.drain()
        await self._notify_all(f'Подключился {username}')

    async def _remove_user(self, username: str) -> None:
        writer = self._username_to_writer[username]
        del self._username_to_writer[username]

        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            print('Ошибка при закрытии клиентского писателя, игнорируется')

    async def _listen_for_messages(
        self, username: str, reader: StreamReader
    ) -> None:
        try:
            while (
                data := await asyncio.wait_for(reader.readline(), 60)
            ) != b'':
                await self._notify_all(f'{username}: {data.decode()}\n')
                await self._notify_all(f'{username} has left the chat\n')
        except Exception:
            print('Ошибка при чтении данных от клиента.')
            await self._remove_user(username)

    async def _notify_all(self, message: str) -> None:
        print(f'Сообщение в рассылке: {message}')
        inactive_users: list[str] = []

        for username, writer in self._username_to_writer.items():
            try:
                writer.write(message.encode())
                await writer.drain()
            except ConnectionError:
                print('Ошибка при записи данных клиенту.')
                inactive_users.append(username)

        [await self._remove_user(username) for username in inactive_users]  # type: ignore[func-returns-value]


async def main() -> None:
    """Run server."""
    chat_server = ChatServer()
    await chat_server.start_chat_server(HOST, PORT)


if __name__ == '__main__':
    asyncio.run(main())
