"""aiohttp views."""

from typing import Annotated

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from dependency_injector.wiring import Provide, inject

from async_ds.di.abstract import AbstractUseCase
from async_ds.di.container import MainContainer
from async_ds.di.routes import routes


@routes.get('/products')  # type: ignore[arg-type]
@inject
async def products(
    request: Request,
    use_case: Annotated[AbstractUseCase, Provide[MainContainer.use_case]],
) -> Response:
    """Render products."""
    result = await use_case.get_products()
    print(f'Success /products request. Products: {result}')
    return web.json_response(result)
