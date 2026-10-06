"""ABC."""

from abc import ABC, abstractmethod
from typing import TypeVar

ProductT = TypeVar('ProductT')


class AbstractRepository[ProductT](ABC):
    """ABC for repository."""

    @abstractmethod
    async def list_all(self) -> list[ProductT]:
        """Get all."""
