"""Test Producer."""

from unittest.mock import Mock

import pytest

from eip.application.messages import Command
from eip.infrastructure.messaging.abstract import (
    AbstractChannel,
    AbstractProducer,
)
from eip.infrastructure.messaging.points import Producer


@pytest.fixture
def mock_channel() -> Mock:
    """Provide channel mock."""
    return Mock(spec=AbstractChannel)


@pytest.fixture
def producer(
    mock_channel: AbstractChannel[Command],
) -> AbstractProducer[Command]:
    """Provide Producer."""
    return Producer(channel=mock_channel)


async def test_producer_sends_command_to_channel(
    command: Command,
    mock_channel: Mock,
    producer: AbstractProducer[Command],
) -> None:
    # Act
    await producer.send(command)

    # Assert
    mock_channel.send.assert_called_once_with(command)
