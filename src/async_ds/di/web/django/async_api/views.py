"""Views."""

import asyncio
from datetime import datetime

import aiohttp
from aiohttp import ClientSession
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


async def get_url_detaile(
    session: ClientSession, url: str
) -> dict[str, str | int]:
    """Get url details."""
    start_time = datetime.now()
    response = await session.get(url)
    response_body = await response.text()
    end_time = datetime.now()
    return {
        'status': response.status,
        'time': (end_time - start_time).microseconds,
        'body_length': len(response_body),
    }


async def make_request(
    url: str, request_num: int
) -> dict[str, list[dict[str, str | int] | BaseException] | list[Exception]]:
    """Make reauest."""
    async with aiohttp.ClientSession() as session:
        requests = [
            get_url_detaile(session, url) for _ in range(0, request_num)
        ]
        results = await asyncio.gather(*requests, return_exceptions=True)

        successful_results = [
            result for result in results if not isinstance(result, Exception)
        ]
        failed_results = [
            result for result in results if isinstance(result, Exception)
        ]

        return {
            'successful_results': successful_results,
            'failed_results': failed_results,
        }


async def requests_view(request: HttpRequest) -> HttpResponse:
    """Handle request."""
    url = request.GET['url']
    request_num: int = int(request.GET['request_num'])
    context = await make_request(url, request_num)
    return render(request, 'async_api/request.html', context=context)
