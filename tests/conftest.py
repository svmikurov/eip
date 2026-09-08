"""Pytest configuration."""

from unittest.mock import Mock

import pytest

from eip.application.messages import Command
from eip.domain.protocols import HandlerProto
from eip.infrastructure.messaging.abstract import (
    AbstractChannel,
    AbstractConsumer,
    AbstractProducer,
)
from eip.infrastructure.messaging.channels import InMemoryQueue
from eip.infrastructure.messaging.points import Consumer, Producer

REQUEST_ID = "123abc"
COMMAND_BODY = "Command body"


@pytest.fixture
def handler() -> Mock:
    """Provide message Handler."""
    return Mock(spec=HandlerProto)


@pytest.fixture
def command() -> Command:
    """Provide command message."""
    return Command(request_id=REQUEST_ID, body=COMMAND_BODY)


# Infrastructure
# ~~~~~~~~~~~~~~


@pytest.fixture
def in_memory_channel() -> AbstractChannel[Command]:
    """Provide in-memory queue."""
    return InMemoryQueue()


@pytest.fixture
def producer(
    in_memory_channel: AbstractChannel[Command],
) -> AbstractProducer[Command]:
    """Provide Producer."""
    return Producer(channel=in_memory_channel)


@pytest.fixture
def consumer(
    in_memory_channel: AbstractChannel[Command],
    handler: HandlerProto[Command],
) -> AbstractConsumer[Command]:
    """Provide message consumer."""
    return Consumer(channel=in_memory_channel, handler=handler)
