"""Клиент чат сервера."""

import asyncio
import os
import sys
import tty
from asyncio import StreamReader, StreamWriter
from typing import Deque

from eip.examples.asyncio.chapter_08.listing_5 import create_stdin_reader
from eip.examples.asyncio.chapter_08.listing_7 import (
    delete_line,
    move_to_bottom_of_screen,
    move_to_top_of_screen,
    restore_cursor_position,
    save_cursor_position,
)
from eip.examples.asyncio.chapter_08.listing_8 import read_line
from eip.examples.asyncio.chapter_08.listing_9 import MessageStore

HOST = '127.0.0.1'
PORT = 8888


async def send_message(message: str, writer: StreamWriter) -> None:
    """Send client message to server."""
    writer.write(message.encode())
    await writer.drain()


async def listen_for_messages(
    reader: StreamReader,
    message_store: MessageStore,
) -> None:
    """Listen a messages from server."""
    while (message := await reader.readline()) != b'':
        await message_store.append(message.decode())
    await message_store.append('Сервер закрыл соединение.')


async def read_and_send(
    stdin_reader: StreamReader, writer: StreamWriter
) -> None:
    """Read and send message."""
    while True:
        message = await read_line(stdin_reader)
        await send_message(message, writer)


async def main() -> None:
    """Run client."""

    async def redraw_output(items: Deque[str]) -> None:
        save_cursor_position()
        move_to_top_of_screen()
        for item in items:
            delete_line()
            sys.stdout.write(item)
        restore_cursor_position()

    tty.setcbreak(0)
    os.system('clear')
    rows = move_to_bottom_of_screen()

    messages = MessageStore(redraw_output, rows - 1)

    stdin_reader = await create_stdin_reader()
    sys.stdout.write('Введите имя пользователя: ')
    username = await read_line(stdin_reader)

    reader, writer = await asyncio.open_connection(HOST, PORT)

    sys.stdout.write('Соединение установлено')

    writer.write(f'CONNECT {username}\n'.encode())
    await writer.drain()

    message_listener = asyncio.create_task(
        listen_for_messages(reader, messages),
    )
    input_listener = asyncio.create_task(
        read_and_send(stdin_reader, writer),
    )

    try:
        await asyncio.wait(
            [message_listener, input_listener],
            return_when=asyncio.FIRST_COMPLETED,
        )
    except Exception as e:
        print(e)
        writer.close()
        await writer.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
