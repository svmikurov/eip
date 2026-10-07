"""Asyncio examples use cases."""

from dataclasses import asdict
from typing import override

from .abstract import AbstractRepository, AbstractUseCase
from .domain import Product


class ProductUseCases(AbstractUseCase):
    """Product use cases."""

    def __init__(self, repo: AbstractRepository[Product]) -> None:
        self._repo = repo

    @override
    async def get_products(self) -> list[dict[str, str | int]]:
        """Get product list."""
        products: list[Product] = await self._repo.list_all()
        return [asdict(product) for product in products]
