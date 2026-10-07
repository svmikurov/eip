"""Подключение к базе данных о товарах."""

from typing import Any

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from asyncpg import Record
from asyncpg.pool import Pool

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
