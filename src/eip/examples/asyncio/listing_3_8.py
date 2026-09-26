"""Построение асинхронного эхо-сервера."""

import asyncio
import socket
from asyncio import AbstractEventLoop


async def echo(
    connection: socket.socket,
    loop: AbstractEventLoop,
) -> None:
    """Return recieved data from echo-server."""
    while data := await loop.sock_recv(connection, 1024):
        await loop.sock_sendall(connection, data)


async def listen_for_connection(
    server_socket: socket.socket,
    loop: AbstractEventLoop,
) -> None:
    """Listen for connection."""
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Получен запрос на подключение от {address}')
        asyncio.create_task(echo(connection, loop))


async def main() -> None:
    """Run serrver."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.bind(server_address)
    server_socket.setblocking(False)
    server_socket.listen()

    await listen_for_connection(server_socket, asyncio.get_event_loop())
