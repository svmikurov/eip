"""Protocols for domain interface."""

from typing import Protocol, TypeVar

MessageT = TypeVar('MessageT')


class HandlerProto[MessageT](Protocol):
    """Protocol for handler interface."""

    def handle(self, message: MessageT) -> None:
        """Handle message."""
