"""Echo server on asyncio."""

import argparse
import asyncio

from eip.examples.socket import conf


async def handle(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    """Handle connection."""
    addr = writer.get_extra_info('peername')
    print(f'Accepted connection from {addr}')

    try:
        while data := await reader.read(conf.MAX_MESSAGE_LEN):
            writer.write(data)
            await writer.drain()

    except ConnectionResetError:
        print(f'Connection reset by {addr}')

    finally:
        print(f'Closing connection to {addr}')
        writer.close()
        await writer.wait_closed()


async def main(host: str, port: int) -> None:
    """Run server."""
    server = await asyncio.start_server(handle, host, port)
    addrs = ', '.join(str(s.getsockname()) for s in server.sockets)
    print(f'Listening on {addrs}')

    async with server:
        await server.serve_forever()


def parse_args() -> argparse.Namespace:
    """Parse args."""
    p = argparse.ArgumentParser(description='Async ech server')
    p.add_argument('host', help='host to bind, e.g. 127.0.0.1')
    p.add_argument('port', help='port to bind, e.g. 8888', type=int)
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()

    try:
        asyncio.run(main(args.host, args.port))

    except KeyboardInterrupt:
        print('Cought keyboard interrapt, existing')
