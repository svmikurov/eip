"""Abstract base classes for Messaging."""

from abc import ABC, abstractmethod
from typing import TypeVar

MessageT = TypeVar('MessageT')


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
    def handle(self, message: MessageT) -> None:
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

    @abstractmethod
    def has_message(self, message: MessageT) -> bool:
        """Check whether the queue has specific message."""

    @property
    @abstractmethod
    def is_full_queue(self) -> bool:
        """Check whether the queue has reached its maximum capacity."""
