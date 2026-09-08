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


def test_channel_receive_message_from_queue(
    command: Command,
    in_memory_channel: AbstractChannel[Command],
) -> None:
    # Arrange
    in_memory_channel.send(command)

    # Act
    message = in_memory_channel.receive()

    # Assert
    assert command not in in_memory_channel.queue
    assert message is not None
    assert message is command
    assert message not in in_memory_channel.queue
