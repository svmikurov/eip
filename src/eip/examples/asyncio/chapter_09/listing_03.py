"""получение конкретного товара."""

from typing import Any

import asyncpg
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from asyncpg import Record
from asyncpg.pool import Pool

DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = '5432'
DATABASE_USER = 'postgres'
DATABASE_PASS = 'password'
DATABASE_NAME = 'eip'
MIN_SIZE = 6
MAX_SIZE = 6

DATABASE_KEY = 'database'
routes = web.RouteTableDef()

QUERY = """
SELECT
product_id,
product_name,
brand_id
FROM product
WHERE product_id = $1
"""


async def create_dtabase_poll(app: Application) -> None:
    """Create a database pool."""
    print('Создается пул подключений.')
    pool: Pool = await asyncpg.create_pool(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USER,
        password=DATABASE_PASS,
        database=DATABASE_NAME,
        min_size=MIN_SIZE,
        max_size=MAX_SIZE,
    )
    app[DATABASE_KEY] = pool


async def destroy_database_pool(app: Application) -> None:
    """Destroy a database pool."""
    print('Уничтожается пул подключений.')
    pool: Pool = app[DATABASE_KEY]
    await pool.close()


@routes.get('/products/')
async def products(request: Request) -> Response:
    """Render products."""
    connection: Pool = request.app[DATABASE_KEY]
    products_query = 'SELECT brand_id, brend_name fron products'
    results: list[Record] = await connection.fetch(products_query)
    result_as_dict: list[dict[str, Any]] = [dict(brend) for brend in results]
    return web.json_response(result_as_dict)


@routes.get('/products/{id}')
async def get_product(request: Request) -> Response:
    """Get product by ID."""
    try:
        url_path_id = request.match_info['id']
        product_id = int(url_path_id)

        connection: Pool = request.app[DATABASE_KEY]
        product: Record | None = await connection.fetchrow(QUERY, product_id)

        if product is not None:
            return web.json_response(dict(product))
        else:
            raise web.HTTPNotFound()

    except ValueError as e:
        raise web.HTTPBadRequest() from e


def main() -> None:
    """Run server."""
    app = web.Application()

    app.on_startup.append(create_dtabase_poll)
    app.on_cleanup.append(destroy_database_pool)

    app.add_routes(routes)
    web.run_app(app)


if __name__ == '__main__':
    main()
