"""Использование протокола."""

import asyncio
from asyncio import AbstractEventLoop
from eip.examples.asyncio.chapter_08.listing_1 import HTTPGetClientTransportProtocol

async def make_request(
    host: str,
    port: int,
    loop: AbstractEventLoop,
) -> str:
    """Make request."""
    def protocol_factory() -> asyncio.Protocol:
        return HTTPGetClientTransportProtocol(host, loop)
    
    _, protocol = await loop.create_connection(
        protocol_factory=protocol_factory, host=host, port=port
    )

    return await protocol.get_response()


async def main() -> None:
    """Run."""
    loop = asyncio.get_running_loop()
    result = await make_request('www.github.com', 80, loop)
    print(result)


asyncio.run(main())