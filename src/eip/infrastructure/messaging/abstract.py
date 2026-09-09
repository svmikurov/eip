"""Abstract base classes for Messaging."""

from abc import ABC, abstractmethod
from typing import TypeVar

MessageT = TypeVar('MessageT')


# Endpoints
# ~~~~~~~~~


class AbstractProducer[MessageT](ABC):
    """ABC for Producer."""

    @abstractmethod
    async def send(self, message: MessageT) -> None:
        """Send message."""


class AbstractConsumer[MessageT](ABC):
    """ABC for Consumer."""

    @abstractmethod
    async def receive(self) -> MessageT:
        """Receive message."""

    @abstractmethod
    async def handle(self, message: MessageT) -> None:
        """Handle message."""

    @abstractmethod
    async def start(self) -> None:
        """Start consumer."""


# Channels
# ~~~~~~~~


class AbstractChannel[MessageT](ABC):
    """ABC for Message Channel."""

    @abstractmethod
    async def send(self, message: MessageT) -> None:
        """Send message."""

    @abstractmethod
    async def receive(self) -> MessageT:
        """Receive message."""

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """Check whether the queue is empty."""

    @property
    @abstractmethod
    def is_full_queue(self) -> bool:
        """Check whether the queue has reached its maximum capacity."""
