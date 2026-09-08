"""Test Producer."""

from eip.application.messages import Command
from eip.infrastructure.messaging.abstract import (
    AbstractProducer,
)


def test_simple_sync_producer(
    producer: AbstractProducer[Command],
) -> None:
    pass
