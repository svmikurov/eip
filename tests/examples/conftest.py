"""Socket example test configuration."""

import socket
import threading
from typing import Generator

import pytest

from eip.examples.socket.multiconn_server import run_server


@pytest.fixture
def host() -> str:
    """Provide connection host."""
    return '127.0.0.1'


@pytest.fixture
def port() -> int:
    """Provide connection port."""
    return 0


@pytest.fixture
def addr(host: str, port: int) -> tuple[str, int]:
    """Provide server connection address."""
    return (host, port)


@pytest.fixture
def server(addr: tuple[str, int]) -> Generator[tuple[str, int], None, None]:
    """Provide tested server."""
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind(addr)

    t = threading.Thread(target=run_server, args=(lsock,), daemon=True)
    t.start()

    yield lsock.getsockname()

    lsock.close()  # ← loop_server бросит OSError → выйдет
