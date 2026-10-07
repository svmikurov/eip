"""Запуск сервера."""

from aiohttp import web
from aiohttp.web_app import Application

from eip.examples.asyncio.di.container import MainContainer

from .entrypoints import routes

DATABASE = {
    'host': '127.0.0.1',
    'port': '5432',
    'user': 'postgres',
    'password': 'password',
    'database': 'postgres',
    'min_size': 6,
    'max_size': 6,
}

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
    container.config.db.from_dict(DATABASE)

    app = web.Application()
    app['container'] = container

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    app.add_routes(routes)
    web.run_app(app)


if __name__ == '__main__':
    main()
