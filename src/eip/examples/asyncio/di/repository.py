"""Repositories."""

from asyncpg import Pool

from .abstract import AbstractRepository
from .domain import Product


class PostgresProductRepository(AbstractRepository[Product]):
    """PostgreSQL product repository."""

    def __init__(self, pool: Pool) -> None:
        self._pool = pool

    async def list_all(self) -> list[Product]:
        """Get all products."""
        query = 'SELECT brand_id, brand_name FROM product'
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [
            Product(brand_id=row['brand_id'], brand_name=row['brand_name'])
            for row in rows
        ]
