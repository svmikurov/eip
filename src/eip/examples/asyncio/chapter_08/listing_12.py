"""Создание эхо-сервера с помощью серверных объектов."""

import asyncio
import logging
from asyncio import StreamReader, StreamWriter

HOST = '127.0.0.1'
PORT = 8000

WRITER_GREETING = 'Добро пожаловать! Число подключенных пользователей: {}\n'
NEW_CLIENT_MSG = 'Подключился новый пользователь!\n'
CLIENT_LOST_MSG = 'Клиент отключился! Осталось пользователейЖ {}!\n'


class ServerState:
    """Server state."""

    def __init__(self) -> None:
        self._writes: list[StreamWriter] = []

    async def add_client(
        self,
        reader: StreamReader,
        writer: StreamWriter,
    ) -> None:
        """Add server client."""
        self._writes.append(writer)
        await self._on_connect(writer)
        asyncio.create_task(self._echo(reader, writer))

    async def _on_connect(self, writer: StreamWriter) -> None:
        """Make on connection event."""
        writer.write(WRITER_GREETING.format(len(self._writes)).encode())
        await writer.drain()
        await self._notify_all(NEW_CLIENT_MSG)

    async def _echo(self, reader: StreamReader, writer: StreamWriter) -> None:
        """Handle client lost."""
        try:
            while (data := await reader.readline()) != b'':
                writer.write(data)
                await writer.drain()

            self._writes.remove(writer)
            await self._notify_all(CLIENT_LOST_MSG.format(len(self._writes)))

        except Exception as e:
            logging.exception('Ошибка чтения данных от клиента.', exc_info=e)
            self._writes.remove(writer)

    async def _notify_all(self, message: str) -> None:
        """Notify all writers."""
        for writer in self._writes:
            try:
                writer.write(message.encode())
                await writer.drain()

            except ConnectionError as e:
                logging.exception('Ошибка записи данных клиенту.', exc_info=e)
                self._writes.remove(writer)  # noqa: B909


async def main() -> None:
    """Run server."""
    server_state = ServerState()

    async def client_conne(
        reader: StreamReader,
        writer: StreamWriter,
    ) -> None:
        await server_state.add_client(reader, writer)

    server = await asyncio.start_server(client_conne, HOST, PORT)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
