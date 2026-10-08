"""Запуск сервера."""

from aiohttp import web
from aiohttp.web_app import Application

from .container import MainContainer
from .routes import routes
from .web.aiohttp import views as aiohttp_views  # noqa: F401  ← ВАЖНО: импорт, чтобы сработали декораторы

DATABASE = {
    'host': '127.0.0.1',
    'port': 5432,
    'user': 'postgres',
    'password': 'password',
    'database': 'postgres',
    'min_size': 6,
    'max_size': 6,
}


def create_container() -> MainContainer:
    """Create main DI container."""
    container = MainContainer()
    container.config.db.from_dict(DATABASE)
    container.wire(modules=['.aiohttp_views'])
    return container


async def on_startup(app: Application) -> None:
    """Create a database pool."""
    container: MainContainer | None = app['container']
    if container is None:
        raise RuntimeError()
    await container.init_resources()  # type: ignore[misc]
    print('Создан пул подключений.')


async def on_cleanup(app: Application) -> None:
    """Destroy a database pool."""
    print('\nУничтожается пул подключений.')
    await app['container'].shutdown_resources()


def main() -> None:
    """Run server."""
    app = web.Application()
    app['container'] = create_container()

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    app.add_routes(routes)
    web.run_app(app)


if __name__ == '__main__':
    main()
