"""Asyncio example DI container."""

import asyncpg
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Resource


class MainContainer(DeclarativeContainer):
    """Asyncio example main container."""

    # ==============================
    # Database connect configuration
    # ==============================
    config = Configuration()
    db_conn_pool = Resource(
        asyncpg.create_pool,
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password,
        database=config.db.name,
        min_size=config.db.min_size,
        max_size=config.db.max_size,
    )
