"""Echo client on asincio."""

import asyncio

from eip.examples.socket import conf

MESSAGES = (b'Hello, world!', b'second line', b'third')


async def main(host: str, port: int) -> None:
    """Run client."""
    reader, writer = await asyncio.open_connection(host, port)
    print(f'Connected to {host}:{port}')

    for message in MESSAGES:
        writer.write(message)
        await writer.drain()
        reply = await reader.read(conf.MAX_MESSAGE_LEN)
        print(f'Received {reply!r}')

    writer.close()
    await writer.wait_closed()


if __name__ == '__main__':
    asyncio.run(main('127.0.0.1', 8888))
