"""Asyncio timed."""

import functools
import time
from typing import Any, Callable


def async_timed() -> Callable:  # type: ignore[type-arg]
    """Time."""

    def wrapper(func: Callable) -> Callable:  # type: ignore[type-arg]
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:  # type: ignore[no-untyped-def]
            print(f'Выполняется {func} с аргументами {args} {kwargs}')

            start_time = time.time()

            try:
                return await func(*args, **kwargs)
            finally:
                end_time = time.time()
                total_time = end_time - start_time
                print(f'{func} завершилась за {total_time:.4f} с')

        return wrapped

    return wrapper
