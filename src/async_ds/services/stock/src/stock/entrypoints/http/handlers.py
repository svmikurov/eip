"""HTTP entrypoint handlers."""

import asyncio
import random

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from .routes import routes


@routes.get('/products/{id}/inventory')
async def get_inventory(request: Request) -> Response:
    """Handle product inventory request."""
    product_id = int(request.match_info['id'])
    inventory = await _get_inventory(product_id)
    return web.json_response({'inventory': inventory})


# TODO: Replace with a real Use Case injected via DI.
async def _get_inventory(product_id: int) -> int:
    """Return a random inventory count (stub)."""
    min_count, max_count = 0, 100
    delay_range = (0, 3)

    delay_seconds = random.uniform(*delay_range)
    await asyncio.sleep(delay_seconds)
    return random.randint(min_count, max_count)
