"""Message channel.

Base messaging component — Message Channel (EIP, p. 93).
"""

from collections import deque
from copy import deepcopy
from typing import TypeVar, override

from .abstract import AbstractChannel
from .exceptions import QueueCircuitOpen

MessageT = TypeVar("MessageT")


class InMemoryQueue(AbstractChannel[MessageT]):
    """In-memory Point-to-Point Channel."""

    DEFAULT_QUEUE_MAX_LEN = 5

    def __init__(
        self,
        queue_max_len: int | None = None,
    ) -> None:
        self._queue_max_len = (
            queue_max_len if queue_max_len is not None else self.DEFAULT_QUEUE_MAX_LEN
        )
        self._queue: deque[MessageT] = deque(maxlen=self._queue_max_len)

    @override
    def send(self, message: MessageT) -> None:
        """Send a message to the channel."""
        # TODO: Add Dead Letter Channel
        if self.is_full_queue:
            raise QueueCircuitOpen
        self._queue.append(message)

    @property
    def queue(self) -> deque[MessageT]:
        """Return a copy of the current message queue."""
        return deepcopy(self._queue)

    @property
    def is_full_queue(self) -> bool:
        """Check whether the queue has reached its maximum capacity."""
        return not len(self._queue) < self._queue_max_len
