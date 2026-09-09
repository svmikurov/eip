"""Message channel.

Base messaging component — Message Channel (EIP, p. 93).
"""

import asyncio
from typing import TypeVar, override

from .abstract import AbstractChannel
from .exceptions import QueueCircuitOpen

MessageT = TypeVar('MessageT')


class InMemoryQueue(AbstractChannel[MessageT]):
    """In-memory Point-to-Point Channel."""

    DEFAULT_QUEUE_MAX_LEN = 5

    def __init__(
        self,
        queue_max_len: int | None = None,
    ) -> None:
        self._queue_max_len = (
            queue_max_len
            if queue_max_len is not None
            else self.DEFAULT_QUEUE_MAX_LEN
        )
        self._queue: asyncio.Queue[MessageT] = asyncio.Queue(
            maxsize=self._queue_max_len
        )

    @override
    async def send(self, message: MessageT) -> None:
        """Send a message to the channel."""
        # TODO: Add Dead Letter Channel
        if self.is_full:
            raise QueueCircuitOpen
        await self._queue.put(message)

    @override
    async def receive(self) -> MessageT:
        """Receive message."""
        return await self._queue.get()

    @property
    @override
    def is_empty(self) -> bool:
        """Check whether the queue is empty."""
        return self._queue.empty()

    @property
    @override
    def is_full(self) -> bool:
        """Check whether the queue has reached its maximum capacity."""
        return self._queue.full()
