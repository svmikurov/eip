"""Sync Polling Consumer tests."""

from unittest.mock import Mock

from eip.application.messages import Command
from eip.infrastructure.messaging.abstract import (
    AbstractConsumer,
    AbstractProducer,
)


def test_handler_consumer_called_with_command(
    command: Command,
    producer: AbstractProducer[Command],
    consumer: AbstractConsumer[Command],
    handler: Mock,
) -> None:
    # Act
    producer.send(command)
    consumer.start()

    # Assert
    handler.handle.assert_called_once_with(command)
