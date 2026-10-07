"""Asyncio examples use cases."""

from dataclasses import asdict

from .domain import Product
from .abstract import AbstractRepository


class ProductUseCases:
    """Product use cases."""

    def __init__(self, repo: AbstractRepository) -> None:
        self._repo = repo

    async def get_products(self) -> list[dict[str, str | int]]:
        """Get product list."""
        products: list[Product] = await self._repo.list_all()
        return [asdict(product) for product in products]