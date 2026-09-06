"""Message channel.

Base messaging component — Message Channel (EIP, p. 93).
"""

from collections import deque
from copy import deepcopy
from typing import TypeVar, override

from .abstract import AbstractReplyQueue, AbstractRequestQueue
from .exceptions import QueueCircuitOpen

MessageT = TypeVar("MessageT")


class InMemoryRequestQueue(AbstractRequestQueue[MessageT]):
    """In-memory Point-to-Point Request channel."""

    DEFAULT_QUEUE_MAX_LEN = 300

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


class InMemoryReplyQueue(AbstractReplyQueue):
    """In-memory Point-to-Point Reply channel."""


class InvalidMessages:
    """Invalid messages queue.

    Used by both requestor and replier to forward malformed or
    unprocessable messages.
    """
