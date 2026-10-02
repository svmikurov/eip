"""Конкурентные веб-запросы."""

from aiohttp import ClientSession

from eip.examples.asyncio.util import async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    """Fetch status."""
    async with session.get(url) as result:
        return result.status
