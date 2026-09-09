"""Polling Consumer tests."""

import asyncio
from unittest.mock import Mock

import pytest

from eip.application.messages import Command
from eip.domain.protocols import HandlerProto
from eip.infrastructure.messaging.abstract import (
    AbstractChannel,
    AbstractConsumer,
    AbstractProducer,
)
from eip.infrastructure.messaging.points import Consumer


@pytest.fixture
def consumer(
    in_memory_channel: AbstractChannel[Command],
    mock_handler: HandlerProto[Command],
) -> AbstractConsumer[Command]:
    """Provide message consumer."""
    return Consumer(channel=in_memory_channel, handler=mock_handler)


async def test_consumer_calls_handler_with_command(
    command: Command,
    producer: AbstractProducer[Command],
    consumer: AbstractConsumer[Command],
    mock_handler: Mock,
) -> None:
    # Arrange
    task = asyncio.create_task(consumer.start())
    await asyncio.sleep(0.1)

    # Act
    await producer.send(command)
    await asyncio.sleep(0.1)

    # Assert
    mock_handler.handle.assert_called_once_with(command)

    # Teardown
    task.cancel()
