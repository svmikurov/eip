"""Abstract base classes for topic channel."""

from abc import ABC, abstractmethod
from typing import TypeVar

MessageT = TypeVar('MessageT')


# General


class AbstractBind(ABC):
    """ABC for channel bind interface."""

    @abstractmethod
    def bind(self, host: str, port: int) -> None:
        """Bind channel."""


class AbstractSend[MessageT](ABC):
    """ABC for send message to channel interface."""

    @abstractmethod
    def send(self, message: MessageT) -> None:
        """Send message."""
