"""Abstract base classes for Message Channels."""

from abc import ABC, abstractmethod
from typing import TypeVar

MessageT = TypeVar("MessageT")


class AbstractRequestQueue[MessageT](ABC):
    """ABC for Point-to-Point Request channel.

    Used by the requestor to send a request message
    to a single replier.
    """

    @abstractmethod
    def send(self, message: MessageT) -> None:
        """Send message to channel."""


class AbstractReplyQueue(ABC):
    """ABC for Point-to-Point Reply channel.

    Used by the replier to send a reply message
    to a single requestor.
    """
