"""Topic server."""

from .abstract import AbstractBind, AbstractSend


class TopicSocketServer(
    AbstractBind,
    AbstractSend[str],
):
    """Topic (queue) channel socket server."""

    def __init__(
        self,
        server: AbstractBind,
        queue: object,
    ) -> None:
        self._server = server
        self._queue = queue

    def bind(self, host: str, port: int) -> None:
        """Bind channel."""
        self._server.bind(host, port)

    def send(self, message: str) -> None:
        """Send message."""
        raise NotImplementedError
