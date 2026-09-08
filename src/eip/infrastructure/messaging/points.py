"""Message Endpoint (EIP, p. 124)."""

from typing import TypeVar

from eip.domain.protocols import HandlerProto
from eip.infrastructure.messaging.abstract import AbstractChannel, AbstractConsumer

from .abstract import AbstractProducer

MessageT = TypeVar("MessageT")


class Producer[MessageT](AbstractProducer):
    """Request initiator."""

    def __init__(
        self,
        channel: AbstractChannel[MessageT],
    ) -> None:
        self._channel = channel

    def send(self, message: MessageT) -> None:
        """Send message."""


class Consumer[MessageT](AbstractConsumer):
    """Consumer."""

    def __init__(
        self,
        channel: AbstractChannel[MessageT],
        handler: HandlerProto[MessageT],
    ) -> None:
        super().__init__()


class Replier:
    """Reply handler for Request-Reply Channel.

    Receives a request message and sends back a reply.
    """
