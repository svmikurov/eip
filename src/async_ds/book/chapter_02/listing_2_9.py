"""Создание задачи."""

import asyncio

from async_ds.book.util import delay


async def main() -> None:
    """Run code."""
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_one_more = asyncio.create_task(delay(3))

    print('Start')

    await sleep_for_three
    await sleep_again
    await sleep_one_more

    print('Stop')


asyncio.run(main())
