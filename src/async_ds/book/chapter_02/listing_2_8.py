"""Создание задачи."""

import asyncio

from async_ds.book.util import delay


async def main() -> None:
    """Run code."""
    sleep_for_three = asyncio.create_task(delay(3))
    print(f'{type(sleep_for_three) = }')
    result = await sleep_for_three
    print(f'{result = }')


asyncio.run(main())
