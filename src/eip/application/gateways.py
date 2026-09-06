"""Messaging Gateways."""

from eip.application import messages, protocols


class Requestor:
    """Request-Reply Channel Requestor in a Messaging Gateway."""

    def __init__(
        self,
        producer: protocols.ProducerProto,
        customer: protocols.ConsumerProto,
        invalid_producer: protocols.ProducerProto,
    ):
        self._producer = producer
        self._customer = customer
        # TODO: Add functionality for invalid producer
        self._invalid_producer = invalid_producer

    async def request(self, request_id: str, content: str) -> str:
        """Request."""
        command_message = messages.PredictionCommand(
            request_id=request_id,
            correlation_id=None,
            reply_to=None,
            body=content,
        )
        await self._producer.send(command_message)
        document_message = await self._customer.receive(request_id)
        return document_message.body


class Replier:
    """Request-Reply Channel Replier in a Messaging Gateway."""
