"""Конечная точка для возврата текущего времени."""

from datetime import datetime

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

routes = web.RouteTableDef()


@routes.get('/time')
async def time(request: Request) -> Response:
    """Return current time."""
    today = datetime.today()
    result = {
        'moth': today.month,
        'day': today.day,
        'time': str(today.time()),
    }
    return web.json_response(result)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)
