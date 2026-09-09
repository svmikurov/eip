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


def test_consumer_received_message_from_channel(
    command: Command,
    in_memory_channel: AbstractChannel[Command],
    consumer: AbstractConsumer[Command],
) -> None:
    # Arrange
    in_memory_channel.send(command)

    # Act
    message = consumer.receive()

    # Assert
    assert message is command
    assert not in_memory_channel.has_message(command)


def test_consumer_call_handler(
    command: Command,
    in_memory_channel: AbstractChannel[Command],
    consumer: AbstractConsumer[Command],
    handler: Mock,
) -> None:
    # Arrange
    in_memory_channel.send(command)

    # Act
    consumer.handle(command)

    # Assert
    handler.handle.assert_called_once_with(command)
