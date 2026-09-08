"""Messaging Gateways."""

from eip.application import messages, protocols


class RequestGateway:
    """Request-Reply Channel Requestor in a Messaging Gateway."""

    def __init__(
        self,
        request_channel: protocols.RequestChannelGateway,
        reply_channel: protocols.ReplyChannelGateway,
        dead_letter_channel: protocols.RequestChannelGateway | None = None,
    ):
        self._request_channel = request_channel
        self._reply_channel = reply_channel
        self._dlq_channel = dead_letter_channel

    async def send_request(self, request_id: str, content: str) -> str:
        """Send request."""
        command_message = messages.PredictionCommand(
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
