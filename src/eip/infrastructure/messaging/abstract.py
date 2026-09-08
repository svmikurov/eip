"""Abstract base classes for Messaging."""

from abc import ABC, abstractmethod
from typing import TypeVar

MessageT = TypeVar("MessageT")


# Endpoints
# ~~~~~~~~~


class AbstractProducer[MessageT](ABC):
    """ABC for Producer."""

    @abstractmethod
    def send(self, message: MessageT) -> None:
        """Send message."""


class AbstractConsumer(ABC):
    """ABC for Consumer."""


# Channels
# ~~~~~~~~


class AbstractChannel[MessageT](ABC):
    """ABC for Message Channel."""

    @abstractmethod
    def send(self, message: MessageT) -> None:
        """Send message."""
