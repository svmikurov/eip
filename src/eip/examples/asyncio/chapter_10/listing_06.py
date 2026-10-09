"""Листинг 10.6. Сервис корзины."""

import functools

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from eip.examples.asyncio.chapter_10.listing_04 import (
    DATABASE_KEY,
    create_database_pool,
    destroy_database_pool,
)

routes = web.RouteTableDef()


@routes.get('/users/{id}/cart')
async def get_card(request: Request) -> Response:
    """Get user cart."""
    try:
        user_id = int(request.match_info['id'])
        db = request.app[DATABASE_KEY]
        cart_query = 'SELECT product_idFROM user_cartWHERE user_id = $1'

        products = await db.fetch(cart_query, user_id)

        if products is not None:
            return web.json_response(dict(product) for product in products)
        else:
            raise web.HTTPNotFound()

    except ValueError as e:
        raise web.HTTPBadRequest() from e


app = web.Application()
app.on_startup.append(
    functools.partial(
        create_database_pool,
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password='password',
        database='cart',
    )
)
app.on_cleanup(destroy_database_pool)
app.add_routes(routes)
web.run_app(app, port=8003)
