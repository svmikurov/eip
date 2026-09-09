"""Messaging Gateways."""

from eip.application.messages import PredictionCommand
from eip.application.protocols import (
    ReplyChannelGateway,
    RequestChannelGateway,
)


class RequestGateway:
    """Request-Reply Channel Requestor in a Messaging Gateway."""

    def __init__(
        self,
        request_channel: RequestChannelGateway[PredictionCommand],
        reply_channel: ReplyChannelGateway[str, PredictionCommand],
        dead_letter_channel: RequestChannelGateway[PredictionCommand] | None = None,
    ):
        self._request_channel = request_channel
        self._reply_channel = reply_channel
        self._dlq_channel = dead_letter_channel

    async def send_request(self, request_id: str, content: str) -> str:
        """Send request."""
        command_message = PredictionCommand(
            request_id=request_id,
            correlation_id=None,
            reply_to=None,
            body=content,
        )
        await self._request_channel.send(command_message)
        document_message = await self._reply_channel.receive(request_id)
        return document_message.body


class ReplyGateway:
    """Request-Reply Channel Replier in a Messaging Gateway."""
