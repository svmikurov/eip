"""Message Endpoint (EIP, p. 124)."""

from eip.application.abstract import AbstractChannel


class Producer:
    """Request initiator for Request-Reply Channel.

    Sends a request message and waits for a reply.
    """

    def __init__(
        self,
        message_channel: AbstractChannel,
    ) -> None:
        self._message_channel = message_channel


class Replier:
    """Reply handler for Request-Reply Channel.

    Receives a request message and sends back a reply.
    """
