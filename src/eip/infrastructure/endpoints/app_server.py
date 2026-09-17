"""Socket server for application example."""

import selectors
import socket
import sys
import traceback

import lib_server

sel = selectors.DefaultSelector()


def accept_wrapper(sock) -> None:
    """Accept wrappers."""
    conn, addr = sock.accept()  # Should be ready to read
    print(f'Accepted connection from {addr}')
    conn.setblocking(False)
    message = lib_server.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} <host> <port>')
    sys.exit(1)

# Получаем хост и порт для запуска сервера
host, port = sys.argv[1], int(sys.argv[2])

# Создаем сокет
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Проблема
# ~~~~~~~~
# Когда сервер закрывается (или падает), операционная система не освобождает порт мгновенно.
# Он остаётся в состоянии TIME_WAIT на некоторое время (обычно от 30 секунд до 4 минут).
# Это сделано для того, чтобы:
# - Убедиться, что все пакеты из старого соединения дошли до адресата
# - Не перепутать пакеты старого соединения с пакетами нового
# Если вы попытаетесь запустить сервер снова сразу после остановки, вы получите ошибку:
# OSError: [Errno 48] Address already in use
# Решение
# ~~~~~~~
# lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Эта строка говорит операционной системе:
# "Разреши повторно использовать этот адрес (хост + порт),
# даже если он ещё находится в состоянии TIME_WAIT".
# SOL_SOCKET    - Уровень сокета (общие опции для всех сокетов)
# SO_REUSEADDR  - Опция "разрешить повторное использование адреса"
# 1             - Включить опцию (0 — выключить)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

lsock.bind((host, port))
lsock.listen()

#####################################
print(f'Listening on {(host, port)}')
#####################################

lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        f'Main: Error: Exception for {message.addr}:\n'
                        f'{traceback.format_exc()}'
                    )
                    message.close()
except KeyboardInterrupt:
    print('Caught keyboard interrupt, exiting')
finally:
    sel.close()
