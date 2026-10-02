"""Отправка веб запроса с помощью aiohttp."""

import asyncio

import aiohttp

from eip.examples.asyncio.chapter_04 import fetch_status
from eip.examples.asyncio.util import async_timed

URL = 'http://mail.ru'


@async_timed()
async def main() -> None:
    """Send request."""
    async with aiohttp.ClientSession() as session:
        status = await fetch_status(session, URL)
        print(f'Состояние для {URL} было равно {status}')


asyncio.run(main())
