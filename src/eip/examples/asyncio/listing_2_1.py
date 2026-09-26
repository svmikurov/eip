"""Использование ключевого слова async."""

import asyncio


async def coroutine_add_one(number: int) -> int:
    """Add one."""
    return number + 1


def add_one(number: int) -> int:
    """Add one."""
    return number + 1


function_result = add_one(1)
coroutine_result = asyncio.run(coroutine_add_one(1))

print(
    f'Результат функции равен {function_result}, '
    f'а его тип: {type(function_result)}'
)
print(
    f'Результат сопрограммы равен {coroutine_result}, '
    f'а его тип: {type(coroutine_result)}'
)
