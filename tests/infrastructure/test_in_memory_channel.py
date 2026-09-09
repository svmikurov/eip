"""In-memory channel tests."""

from eip.application.messages import Command
from eip.infrastructure.messaging.abstract import AbstractChannel


def test_channel_added_message_to_queue(
    command: Command,
    in_memory_channel: AbstractChannel[Command],
) -> None:
    # Act
    in_memory_channel.send(command)

    # Assert
    assert in_memory_channel.has_message(command)


def test_channel_receive_message_from_queue(
    command: Command,
    in_memory_channel: AbstractChannel[Command],
) -> None:
    # Arrange
    in_memory_channel.send(command)

    # Act
    message = in_memory_channel.receive()

    # Assert
    assert message is not None
    assert message is command
    assert not in_memory_channel.has_message(command)
