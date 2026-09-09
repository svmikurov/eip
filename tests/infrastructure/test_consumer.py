"""Consumer tests."""

from unittest.mock import Mock

import pytest

from eip.application.messages import Command
from eip.domain.protocols import HandlerProto
from eip.infrastructure.messaging.abstract import (
    AbstractChannel,
    AbstractConsumer,
)
from eip.infrastructure.messaging.points import Consumer


@pytest.fixture
def consumer(
    in_memory_channel: AbstractChannel[Command],
    handler: HandlerProto[Command],
) -> AbstractConsumer[Command]:
    """Provide consumer."""
    return Consumer(channel=in_memory_channel, handler=handler)


async def test_consumer_receives_message_from_channel_and_removes_it(
    command: Command,
    in_memory_channel: AbstractChannel[Command],
    consumer: AbstractConsumer[Command],
) -> None:
    # Arrange
    await in_memory_channel.send(command)

    # Act
    message = await consumer.receive()

    # Assert
    assert message is command
    assert in_memory_channel.is_empty


async def test_consumer_calls_handler_when_message_received(
    command: Command,
    in_memory_channel: AbstractChannel[Command],
    consumer: AbstractConsumer[Command],
    handler: Mock,
) -> None:
    # Arrange
    await in_memory_channel.send(command)

    # Act
    await consumer.handle(command)

    # Assert
    handler.handle.assert_called_once_with(command)
