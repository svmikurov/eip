"""Выполнение двух сопрограмм."""

import asyncio

from async_ds.book.util import delay


async def add_one(number: int) -> int:
    """Add one."""
    return number + 1


async def hello_world_message() -> str:
    """Hello Word."""
    await delay(1)
    return 'Hello Word!'


async def main() -> None:
    """Run code."""
    message = await hello_world_message()
    one_plus_obe = await add_one(1)
    print(one_plus_obe)
    print(message)


asyncio.run(main())
