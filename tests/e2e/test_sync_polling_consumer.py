"""Sync Polling Consumer tests."""

from unittest.mock import Mock

from eip.application.messages import Command
from eip.infrastructure.messaging.abstract import (
    AbstractProducer,
)


def test_handler_consumer_called_with_command(
    command: Command,
    producer: AbstractProducer[Command],
    handler: Mock,
) -> None:
    # Act
    producer.send(command)

    # Assert
    handler.handle.assert_called_once_with(command)
