"""HTTP-запроса с помощью транспортного механизма и протокола."""

import asyncio
from asyncio import AbstractEventLoop, Future, Transport


class HTTPGetClientTransportProtocol(asyncio.Protocol):
    """HTTP client GET method transport protocol."""

    def __init__(
        self,
        host: str,
        loop: AbstractEventLoop,
    ) -> None:
        self._host: str = host
        self._future: Future = loop.create_future()  # type: ignore[type-arg]
        self._transport: Transport | None = None
        self._response_buffer: bytes = b''

    async def get_response(self) -> Future:  # type: ignore[type-arg]
        """Get response.

        Ждать внутренний будущий объект,
        пока не будет получен ответ от сервера.
        """
        return await self._future  # type: ignore[no-any-return]

    def _get_request_bytes(self) -> bytes:
        """Get request bytes."""
        request = (
            f'GET / HTTP/1.1\r\n'
            f'Connection: close\r\n'
            f'Host: {self._host}\r\n\r\n'
        )
        return request.encode()

    def connection_made(self, transport: Transport) -> None:  # type: ignore[override]
        """Call when a connection is made."""
        print(f'Создано подключение к {self._host}')
        self._transport = transport
        # После того как подключение установлено,
        # использовать транспорт для отправки запроса.
        self._transport.write(self._get_request_bytes())

    def data_received(self, data: bytes) -> None:
        """Call when some data is received."""
        print('Получены данные!')
        # Получив данные, сохранить их во внутреннем буфере.
        self._response_buffer += data

    def eof_received(self) -> bool | None:
        """Call when the other end calls write_eof() or equivalent."""
        # После закрытия подключения завершить будущий объект,
        # скопировав в него данные из буфера.
        self._future.set_result(self._response_buffer.decode())
        return False

    def connection_lost(self, exc: Exception | None) -> None:
        """Call when the connection is lost or closed."""
        if exc is None:
            print('Подключение закрыто без ошибок.')
        else:
            self._future.set_exception(exc)
