"""Abstract base classes for Messaging."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar

MessageT = TypeVar("MessageT")


# Endpoints
# ~~~~~~~~~


class AbstractProducer[MessageT](ABC):
    """ABC for Producer."""

    @abstractmethod
    def send(self, message: MessageT) -> None:
        """Send message."""


class AbstractConsumer[MessageT](ABC):
    """ABC for Consumer."""

    @abstractmethod
    def receive(self) -> MessageT:
        """Receive message."""

    @abstractmethod
    def handle(self, message: MessageT) -> MessageT:
        """Handle message."""

    @abstractmethod
    def start(self) -> None:
        """Start consumer."""


# Channels
# ~~~~~~~~


class AbstractChannel[MessageT](ABC):
    """ABC for Message Channel."""

    @abstractmethod
    def send(self, message: MessageT) -> None:
        """Send message."""

    @abstractmethod
    def receive(self) -> MessageT:
        """Receive message."""

    @property
    @abstractmethod
    def queue(self) -> Sequence[MessageT]:
        """Return a copy of the current message queue."""
