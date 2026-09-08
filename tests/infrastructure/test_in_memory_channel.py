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
    assert command in in_memory_channel.queue
