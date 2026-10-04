"""Создание эхо-сервера с помощью серверных объектов."""

import asyncio

HOST = '127.0.0.1'
PORT = 8888


class ServerState:
    """Состояние эхо-сервера."""

    def __init__(self) -> None:
        # Состояние хранит открытые подключенным клиентам
        # каналы для отправки клиентам сообщений.
        self._writers: list[asyncio.StreamWriter] = []

    async def add_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        """Добавь вновь подключенного клиента. """
        self._writers.append(writer)
        await self._on_connect(writer)
        asyncio.create_task(self._echo(reader, writer))

    async def _echo(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        try:
            while (data := await reader.read()) != b'':
                writer.write(data)
                await writer.drain()
            
            self._writers.remove(writer)
            await self._notify_all(
                 f'Клиент отключился! Осталось пользователей: '
                 f'{len(self._writers)}!\n'
            )

        except Exception as e:
            print('Ошибка чтения данных от клиента')
            self._writers.remove(writer)

    async def _on_connect(self, writer: asyncio.StreamWriter) -> None:
        """Запускает регламент при подключении нового клиента."""
        writer.write(
            f'Добро пожаловать! Число подключенных пользователей: '
            f'{len(self._writers)}\n'.encode()
        )
        await writer.drain()
        await self._notify_all('Подключился новый пользователь!\n')

    async def _notify_all(self, message: str) -> None:
        """Уведоми всех подключенных клиентов."""
        for writer in self._writers:
            try:
                writer.write(f'{message}'.encode())
                await writer.drain()
            except ConnectionError as e:
                print(
                    'Ошибка записи данных клиенту. '
                    'Клиент удаляется из списка подключенных.'
                )
                self._writers.remove(writer)


async def main() -> None:
    """Запусти сервер."""
    server_state = ServerState()

    async def client_connected_cb(
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        """Обработай событие подключения клиента."""
        await server_state.add_client(reader, writer)

    server = await asyncio.start_server(client_connected_cb, HOST, PORT)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
