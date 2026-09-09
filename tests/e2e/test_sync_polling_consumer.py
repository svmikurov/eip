"""Polling Consumer tests."""

from unittest.mock import Mock

from eip.application.messages import Command
from eip.infrastructure.messaging.abstract import (
    AbstractConsumer,
    AbstractProducer,
)


async def test_consumer_calls_handler_with_command(
    command: Command,
    producer: AbstractProducer[Command],
    consumer: AbstractConsumer[Command],
    handler: Mock,
) -> None:
    # Act
    await producer.send(command)
    await consumer.start()

    # Assert
    handler.handle.assert_called_once_with(command)
