"""Листинг 10-5. Сервис избранного."""

import functools

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from async_ds.book.chapter_10.listing_04 import (
    DATABASE_KEY,
    create_database_pool,
    destroy_database_pool,
)

routes = web.RouteTableDef()


@routes.get('/users/{id}/favorites')
async def get_favorites(requset: Request) -> Response:
    """Get user favorites products."""
    try:
        user_id = int(requset.match_info['id'])
        db = requset.app[DATABASE_KEY]
        favorites_query = (
            'SELECT product_idFROM user_favoritesWHERE user_id = $1'
        )

        result = await db.fetch(favorites_query, user_id)

        if result is not None:
            return web.json_response(dict(record) for record in result)
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
        database='favorites',
    )
)
app.on_cleanup.append(destroy_database_pool)
app.add_routes(routes)
web.run_app(app, port=8002)
