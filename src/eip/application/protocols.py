"""Protocols for application interface."""

from typing import Protocol, TypeVar

Query_co = TypeVar('Query_co', covariant=True)
Command_contra = TypeVar('Command_contra', contravariant=True)
Command_co = TypeVar('Command_co', covariant=True)
RequestID_contra = TypeVar('RequestID_contra', contravariant=True)
Document_co = TypeVar('Document_co', covariant=True)


class MessageProto(Protocol):
    """Protocol for message interface."""

    # Header
    @property
    def request_id(self) -> str: ...
    @property
    def correlation_id(self) -> str | None: ...
    @property
    def replay_to(self) -> str | None: ...


class CommandProto(
    MessageProto,
    Protocol[Query_co],
):
    """Protocol for command message interface."""

    # Body
    @property
    def body(self) -> Query_co: ...


class DocumentMessage(
    MessageProto,
    Protocol[Document_co],
):
    """Protocol for document message."""

    # Body
    @property
    def body(self) -> Document_co: ...


class RequestChannelGateway(Protocol[Command_contra]):
    """Protocol for message request channel."""

    async def send(self, message: Command_contra) -> None: ...


class ReplyChannelGateway(Protocol[RequestID_contra, Document_co]):
    """Protocol for message request channel."""

    async def receive(self, request_id: RequestID_contra) -> Document_co: ...


class ConsumerProto(Protocol[Document_co]):
    """Protocol for consumer interface."""

    async def receive(
        self, request_id: str
    ) -> DocumentMessage[Document_co]: ...


class ProducerProto(Protocol[Command_contra]):
    """Protocol for producer interface."""

    async def send(self, command: Command_contra) -> None: ...


class RequesterProto(Protocol):
    """Protocol for requester interface."""


class ReplierProto(Protocol):
    """Protocol for replier interface."""
