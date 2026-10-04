"""Message storage."""

from collections import deque
from typing import Awaitable, Callable, Deque


class MessageStore:
    """Message storage."""

    def __init__(
        self,
        callback: Callable[[Deque[str]], Awaitable[None]],
        max_size: int,
    ) -> None:
        self._deque: Deque[str] = deque(maxlen=max_size)
        self._callback = callback

    async def append(self, message: str) -> None:
        """Add message to store."""
        self._deque.append(message)
