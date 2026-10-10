"""Starlette application.

Note: TODO сгенерированы ИИ для улучшения качества кода и дальнейшего
изучения темы.
"""

import asyncio
from typing import Any, override

from starlette.applications import Starlette
from starlette.datastructures import State
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket


class UserCounter(WebSocketEndpoint):
    """Broadcast the number of connected clients over WebSocket."""

    encoding = 'text'

    # TODO: sockets — общий per-class список, это осознанный реестр
    # всех соединений. Но:
    #   1) list.remove() — O(n) и падает ValueError, если сокета
    #      уже нет; лучше set + discard, либо явная проверка
    #      `if sock in sockets`.
    #   2) мутация списка во время итерации в _send_count() безопасна
    #      только потому, что итерация закончилась до удаления.
    #      Если _send_count вызовут параллельно из двух мест —
    #      будет гонка.
    #   3) в многопроцессном режиме (uvicorn --workers N) каждый
    #      воркер видит только своих клиентов; для общего счётчика
    #      нужен Redis pub/sub или другой брокер.
    sockets: list[WebSocket] = []

    @override
    async def on_connect(self, websocket: WebSocket[State]) -> None:
        """Handle a new client connection."""
        # TODO: сейчас accept() вызывается без проверок. Если
        # понадобится аутентификация/права/лимиты — делать их ДО
        # accept() и при провале звать websocket.close(code=1008)
        # и return.
        await websocket.accept()
        UserCounter.sockets.append(websocket)
        await self._send_count()

    @override
    async def on_disconnect(
        self, websocket: WebSocket[State], close_code: int
    ) -> None:
        """Handle the client closing the connection."""
        # TODO: remove() бросит ValueError, если сокет уже удалён
        # в _send_count() из-за ошибки отправки. Безопаснее:
        #   if websocket in UserCounter.sockets:
        #       UserCounter.sockets.remove(websocket)
        # либо set.discard(websocket).
        UserCounter.sockets.remove(websocket)
        await self._send_count()

    @override
    async def on_receive(self, websocket: WebSocket[State], data: Any) -> None:
        """Handle an incoming message from the client."""
        # TODO: явный close(1003) = "Unsupported Data" — это
        # корректный контракт для read-only эндпоинта. Без
        # переопределения on_receive Starlette делает то же самое
        # по умолчанию. Оставлено намеренно, чтобы контракт был
        # виден читателю.
        await websocket.close(code=1003)

    async def _send_count(self) -> None:
        """Send client count to every connected socket."""
        count = len(UserCounter.sockets)

        if count > 0:
            count_str = str(count)
            # TODO: broadcast через create_task на каждый сокет — ок,
            # но:
            #   1) asyncio.wait(dict) работает (итерируется по ключам),
            #      но неявно; лучше asyncio.wait(list(task_to_sock))
            #      или .keys().
            #   2) нет таймаута — если один send_text завис
            #      (backpressure у медленного клиента), asyncio.wait
            #      будет ждать вечно. Рассмотреть
            #      asyncio.wait(..., timeout=...).
            #   3) asyncio.wait считается менее предпочтительным,
            #      чем asyncio.TaskGroup (3.11+) или asyncio.gather.
            #   4) task.exception() бросит CancelledError, если задача
            #      отменена. Стоит проверять task.cancelled() отдельно.
            #   5) прочитанное исключение не логируется — упадёт в
            #      "Task exception was never retrieved". Добавить
            #      logger.warning(...).
            task_to_sock = {
                asyncio.create_task(websocket.send_text(count_str)): websocket
                for websocket in UserCounter.sockets
            }

            done, _ = await asyncio.wait(task_to_sock)
            for task in done:
                sock = task_to_sock[task]

                if task.exception() is not None:
                    if sock in UserCounter.sockets:
                        UserCounter.sockets.remove(sock)

            # TODO (опционально): после вычистки мёртвых сокетов
            # имеет смысл повторно разослать актуальный count
            # оставшимся клиентам — иначе у них на экране будет
            # устаревшее число.


app = Starlette(
    routes=[
        WebSocketRoute('/counter', UserCounter),
    ],
)
