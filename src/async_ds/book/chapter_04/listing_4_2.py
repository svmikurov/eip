"""Отправка веб запроса с помощью aiohttp."""

import asyncio

import aiohttp

from async_ds.book.util import async_timed

from . import fetch_status

URL = 'http://mail.ru'


@async_timed()
async def main() -> None:
    """Send request."""
    async with aiohttp.ClientSession() as session:
        status = await fetch_status(session, URL)
        print(f'Состояние для {URL} было равно {status}')


asyncio.run(main())
