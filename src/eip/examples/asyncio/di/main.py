"""Запуск сервера."""

from typing import Any

from aiohttp import web
from aiohttp.web_app import Application
from .entrypoints import routes

from eip.examples.asyncio.di.container import MainContainer

DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = '5432'
DATABASE_USER = 'postgres'
DATABASE_PASS = 'password'
DATABASE_NAME = 'postgres'
MIN_SIZE = 6
MAX_SIZE = 6

DATABASE_KEY = 'database'


async def on_startup(app: Application) -> None:
    """Create a database pool."""
    container = app['container']
    await container.init_resources()
    app[DATABASE_KEY] = await container.db_conn_pool()
    app[DATABASE_KEY] = await container.db_conn_pool()


async def on_cleanup(app: Application) -> None:
    """Destroy a database pool."""
    print('\nУничтожается пул подключений.')
    await app['container'].shutdown_resources()


def main() -> None:
    """Run server."""
    container = MainContainer()
    container.config.db.host.from_value('127.0.0.1')
    container.config.db.port.from_value(5432)
    container.config.db.user.from_value('postgres')
    container.config.db.password.from_value('password')
    container.config.db.name.from_value('postgres')
    container.config.db.min_size.from_value(6)
    container.config.db.max_size.from_value(6)

    app = web.Application()
    app['container'] = container

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    app.add_routes(routes)
    web.run_app(app)


if __name__ == '__main__':
    main()
