"""FastAPI entrypoint."""

from fastapi import FastAPI

app = FastAPI()


def read_root() -> None:
    """Return root."""
    pass
