"""Echo client on asincio."""

import argparse
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


def parse_args() -> argparse.Namespace:
    """Parse args."""
    p = argparse.ArgumentParser(description='Async echo client')
    p.add_argument('host', help='server host, e.g. 127.0.0.1')
    p.add_argument('port', help='server port, e.g. 8888', type=int)
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    asyncio.run(main(args.host, args.port))
