"""Подключение к базе данных о товарах."""

from typing import Any

from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from asyncpg import Record
from asyncpg.pool import Pool

from eip.examples.asyncio.di.container import MainContainer

DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = '5432'
DATABASE_USER = 'postgres'
DATABASE_PASS = 'password'
DATABASE_NAME = 'postgres'
MIN_SIZE = 6
MAX_SIZE = 6

DATABASE_KEY = 'database'
routes = web.RouteTableDef()


@routes.get('/products')
async def products(request: Request) -> Response:
    """Render products."""
    connection: Pool = request.app[DATABASE_KEY]
    products_query = 'SELECT product_id, product_name from product'
    results: list[Record] = await connection.fetch(products_query)
    result_as_dict: list[dict[str, Any]] = [dict(brand) for brand in results]
    print(f'Server data: {result_as_dict = }')
    return web.json_response(result_as_dict)


async def on_startup(app: Application) -> None:
    """Create a database pool."""
    container = app['container']
    await container.init_resources()
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
