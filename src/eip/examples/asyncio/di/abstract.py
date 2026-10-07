"""ABC."""

from abc import ABC, abstractmethod


class AbstractRepository[ProductT](ABC):
    """ABC for repository."""

    @abstractmethod
    async def list_all(self) -> list[ProductT]:
        """Get all."""


class AbstractUseCase(ABC):
    """Abstract Use Case."""

    @abstractmethod
    async def get_products(self) -> list[dict[str, str | int]]:
        """Get product list."""
