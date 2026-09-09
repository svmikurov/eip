"""In-memory channel tests."""

from eip.application.messages import Command
from eip.infrastructure.messaging.abstract import AbstractChannel


async def test_channel_adds_message_to_queue(
    command: Command,
    in_memory_channel: AbstractChannel[Command],
) -> None:
    # Act
    await in_memory_channel.send(command)

    # Assert
    assert not in_memory_channel.is_empty


async def test_channel_removes_message_from_queue_on_receive(
    command: Command,
    in_memory_channel: AbstractChannel[Command],
) -> None:
    # Arrange
    await in_memory_channel.send(command)

    # Act
    message = await in_memory_channel.receive()

    # Assert
    assert message is not None
    assert message is command
    assert in_memory_channel.is_empty
