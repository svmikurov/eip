"""Подключение к базе данных PostgreSQL."""

import asyncio

import asyncpg


async def main() -> None:
    """Connect to database."""
    connection = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        database='eip',
        password='password',
    )
    version = connection.get_server_version()
    print(f'Подключено! Версия Postgres: {version}')
    await connection.close()


if __name__ == '__main__':
    asyncio.run(main())
