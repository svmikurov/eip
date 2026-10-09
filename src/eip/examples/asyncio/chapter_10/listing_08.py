"""Листинг 10.8. Сервис backend-for-frontend для товаров."""

import asyncio
import logging
from asyncio import Task
from typing import Any, Iterable

import aiohttp
from aiohttp import ClientSession, web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

PRODUCT_BASE = 'http://127.0.0.1:8000'
INVENTORY_BASE = 'http://127.0.0.1:8001'
FAVORITE_BASE = 'http://127.0.0.1:8002'
CART_BASE = 'http://127.0.0.1:8003'

TIMEOUT = 1.0


routes = web.RouteTableDef()


@routes.get('/products')
async def get_products(request: Request) -> Response:
    """Get all products."""
    response = await _request_services()
    return response


async def _request_services() -> Response:
    """Request bounded services."""
    async with aiohttp.ClientSession() as session:
        products = _create_request(
            session, f'/{FAVORITE_BASE}/users/3/products'
        )
        favorites = _create_request(
            session, f'/{FAVORITE_BASE}/users/3/favorites'
        )
        cart = _create_request(session, f'/{CART_BASE}/users/r/cart')

        requests: list[Task[Any]] = [products, favorites, cart]

        done, pending = await asyncio.wait(requests, timeout=TIMEOUT)

        if products in pending:
            _cancel_requests(requests)
            return web.json_response(
                {'error': 'Неудалось подлючится к серверу товаров.'}
            )
        elif products in done and products.exception() is not None:
            _cancel_requests(requests)
            logging.exception(
                'Ошибка сервера при подключении к сервису товаров.'
            )
            return web.json_response(
                {'error': 'Ошибка сервера при подключении к сервису товаров.'},
                status=500,
            )
        else:
            product_response = await products.result().json()

            product_results: list[
                dict[str, int | None]
            ] = await get_products_with_inventory(session, product_response)
            cart_item_count = await get_response_item_count(
                cart, done, pending, 'Error getting user curt.'
            )
            favorite_item_count = await get_response_item_count(
                favorites, done, pending, 'Error getting userfavorites.'
            )

            return web.json_response(
                {
                    'cart_items': cart_item_count,
                    'favorite_items': favorite_item_count,
                    'products': product_results,
                }
            )


async def get_products_with_inventory(
    session: ClientSession,
    product_response: list[dict[str, Any]],
) -> list[dict[str, int | None]]:
    """Get product with inventory."""

    def get_inventory(
        session: ClientSession,
        product_id: str,
    ) -> Task[Any]:
        url = f'{INVENTORY_BASE}/products/{product_id}/inventory'
        return asyncio.create_task(session.get(url))

    def create_product_record(
        product_id: int,
        inventory: int | None,
    ) -> dict[str, int | None]:
        return {'product_id': product_id, 'inventory': inventory}

    inventory_tasks_to_product_id = {
        get_inventory(session, product['product_id']): product['product_id']
        for product in product_response
    }

    inventory_done, inventory_pending = await asyncio.wait(
        inventory_tasks_to_product_id.keys(),
        timeout=TIMEOUT,
    )

    product_results = []

    for done_task in inventory_done:
        product_id = inventory_tasks_to_product_id[done_task]

        if done_task.exception() is None:
            inventory = await done_task.result().json()
            product_results.append(
                create_product_record(
                    product_id,
                    inventory['inventory'],
                )
            )
        else:
            product_results.append(create_product_record(product_id, None))
            logging.exception(
                f'Не удвлось получить сведения о наличии товапа {product_id}',
                exc_info=inventory_tasks_to_product_id[done_task].exception(),
            )

    for pending_task in inventory_pending:
        pending_task.cancel()
        product_id = inventory_tasks_to_product_id[done_task]
        product_results.append(create_product_record(product_id, None))

    return product_results


async def get_response_item_count(
    task: Task[Any],
    done: set[Task[Any]],
    pendig: set[Task[Any]],
    error_msg: str,
) -> int | None:
    """Get response item count."""
    if task in done and task.exception() is None:
        return len(await task.result().json())
    elif task in pendig:
        task.cancel()
        return None
    else:
        logging.exception(error_msg, exc_info=task.exception())
        return None


def _create_request(session: ClientSession, addr: str) -> Task[Any]:
    return asyncio.create_task(session.get(addr))


def _cancel_requests(requests: Iterable[Task[Any]]) -> None:
    [request.cancel() for request in requests]


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=9000)
