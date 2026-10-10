"""Чтение из стандартного ввода по оному символу."""

import sys
from asyncio import StreamReader
from collections import deque
from typing import Deque

from .listing_7 import clear_line, move_back_one_char


async def read_line(stdin_reader: StreamReader) -> str:
    """Read line."""

    def erase_last_char() -> None:
        move_back_one_char()
        sys.stdout.write(' ')
        move_back_one_char()

    delete_char = b'\x7f'
    input_buffer: Deque[bytes] = deque()
    while (input_char := await stdin_reader.read(1)) != b'\n':
        if input_char == delete_char:
            if len(input_buffer) > 0:
                input_buffer.pop()
                erase_last_char()
                sys.stdout.flush()
        else:
            input_buffer.append(input_char)
            sys.stdout.write(input_char.decode())
            sys.stdout.flush()
    clear_line()
    return b''.join(input_buffer).decode()
