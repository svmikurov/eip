"""Message Endpoint (EIP, p. 124)."""

from typing import TypeVar, override

from eip.domain.protocols import HandlerProto
from eip.infrastructure.messaging.abstract import (
    AbstractChannel,
    AbstractConsumer,
)

from .abstract import AbstractProducer

MessageT = TypeVar('MessageT')


class Producer(AbstractProducer[MessageT]):
    """Request initiator."""

    def __init__(
        self,
        channel: AbstractChannel[MessageT],
    ) -> None:
        self._channel = channel

    @override
    def send(self, message: MessageT) -> None:
        """Send message."""
        self._channel.send(message)


class Consumer(AbstractConsumer[MessageT]):
    """Consumer."""

    def __init__(
        self,
        channel: AbstractChannel[MessageT],
        handler: HandlerProto[MessageT],
    ) -> None:
        self._channel = channel
        self._handler = handler
        self._got_message = False

    @override
    def receive(self) -> MessageT:
        """Receive message."""
        return self._channel.receive()

    @override
    def handle(self, message: MessageT) -> None:
        """Handle message."""
        self._handler.handle(message)

    def start(self) -> None:
        """Start consumer."""
        self._got_message = False
        while not self._got_message:
            message = self.receive()
            if message:
                self._handler.handle(message)
                self._got_message = True


class Replier:
    """Reply handler for Request-Reply Channel.

    Receives a request message and sends back a reply.
    """
