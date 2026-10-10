"""Листинг 10-4.

Создание и уничтожение пкла подключений к базе данных.
"""

import asyncpg
from aiohttp.web_app import Application
from asyncpg.pool import Pool

DATABASE_KEY = 'database'


async def create_database_pool(
    app: Application,
    host: str,
    port: int,
    user: str,
    database: str,
    password: str,
) -> None:
    """Create a database poll."""
    pool: Pool = await asyncpg.create_pool(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        min_size=6,
        max_size=6,
    )
    app[DATABASE_KEY] = pool


async def destroy_database_pool(app: Application) -> None:
    """Destroy database pool."""
    pool = app[DATABASE_KEY]
    pool.close()
