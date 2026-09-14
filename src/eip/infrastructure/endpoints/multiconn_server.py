"""Multi-connection socket server.

Source: https://realpython.com/python-sockets

Echo server built on selectors: accepts multiple clients
at once and sends each client back the data it sent.
"""

import selectors
import socket
import sys
import types
from typing import cast

sel = selectors.DefaultSelector()


##############################################################################
# Utility functions


def accept_wrapper(sock: socket.socket) -> None:
    """Accept an incoming connection and register it.

    sock : socket.socket
        The listening socket returned by socket.socket().
        It must already be registered in the selector
        and ready for reading (EVENT_READ).
    """
    # Сокет готов к чтению — значит, есть входящее соединение.
    conn, addr = sock.accept()

    print(f'Accepted connection from {addr}')

    # Неблокирующий режим: recv()/send() не должны
    # останавливать главный цикл.
    conn.setblocking(False)

    # Данные, привязанные к сокету:
    #   addr — адрес клиента
    #   inb  — буфер принятых, но не обработанных байтов
    #   outb — буфер байтов, ожидающих отправки клиенту
    #
    # Буферы пустые (b''), т.к. соединение только принято:
    # обмена данными ещё не было. Наполняются в
    # service_connection() — inb из recv(), outb из inb.
    # Тип bytes (не str) — под recv()/send().
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')

    # Нужно знать и когда клиент прислал данные (EVENT_READ),
    # и когда сокет готов принять данные (EVENT_WRITE).
    # Маска событий собирается побитовым ИЛИ.
    events = selectors.EVENT_READ | selectors.EVENT_WRITE

    sel.register(conn, events, data=data)


def service_connection(
    key: selectors.SelectorKey,
    mask: int,
) -> None:
    """Service a connection that is ready for I/O.

    key : selectors.SelectorKey
        fileobj - the registered socket
        data    - SimpleNamespace with addr, inb, outb
    mask : int
        Bitmask of ready events (EVENT_READ, EVENT_WRITE).
    """
    # key.fileobj типизирован как FileObject (сокет, файл,
    # pipe и т.п.). Для клиентского соединения это всегда
    # socket — сужаем тип через cast, чтобы mypy разрешил
    # sock.recv()/sock.send().
    sock = cast(socket.socket, key.fileobj)

    # key.data имеет тип Any; приводим к types.SimpleNamespace,
    # чтобы явно показать намерение. Имена полей (addr, inb,
    # outb) проверяются только в рантайме.
    data = cast(types.SimpleNamespace, key.data)

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Сокет готов к чтению
        if recv_data:
            # Накапливаем принятые байты в буфере отправки:
            # эхо-сервер вернёт их клиенту, когда сокет
            # будет готов к записи.
            data.outb += recv_data
        else:
            # recv() вернул b'' — клиент закрыл соединение.
            # Закрываем и свою сторону, но сначала снимаем
            # сокет с учёта в селекторе, иначе select()
            # продолжит его отслеживать.
            print(f'Closing connection to {data.addr}')
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f'Echoing {data.outb!r} to {data.addr}')

            # Сокет готов принять порцию данных для отправки.
            # send() может отправить меньше, чем лежит в буфере
            # (например, если буфер отправки сокета заполнен),
            # поэтому ориентируемся на возвращённое число байт.
            sent = sock.send(data.outb)

            # Удаляем из буфера уже отправленные байты;
            # остаток будет отправлен при следующем EVENT_WRITE.
            data.outb = data.outb[sent:]


##############################################################################
# Socket server


host, port = sys.argv[1], int(sys.argv[2])

# listening socket
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()

print(f'Listening on {(host, port)}')

# Прослушивающий сокет тоже делаем неблокирующим.
lsock.setblocking(False)

# Регистрируем прослушивающий сокет в селекторе.
# Отслеживаем только событие чтения: новое соединение —
# это «данные, доступные для чтения» на listen-сокете.
# data=None — маркер того, что это listen-сокет, а не
# клиентское соединение, поэтому буферы к нему
# не привязываем.
sel.register(lsock, selectors.EVENT_READ, data=None)


try:
    while True:
        # select() блокируется (timeout=None), пока не появятся
        # сокеты, готовые к вводу-выводу. Возвращает список
        # кортежей (SelectorKey, mask) — по одному на каждый
        # готовый сокет.
        # https://docs.python.org/3/library/selectors.html
        #   #selectors.SelectorKey
        events = sel.select(timeout=None)

        for key, mask in events:
            if key.data is None:
                # data=None — событие пришло от прослушивающего
                # сокета, значит, есть новое входящее соединение.
                # accept_wrapper() примет его и зарегистрирует.
                #
                # key.fileobj имеет тип FileObject (сокет, файл,
                # pipe и т.п.); для listen-сокета это всегда socket,
                # но анализатор об этом не знает — сужаем через cast.
                accept_wrapper(cast(socket.socket, key.fileobj))
            else:
                # data не None — это уже принятое клиентское
                # соединение, обслуживаем его чтение/запись.
                service_connection(key, mask)
except KeyboardInterrupt:
    print('Caught keyboard interrupt, exiting')
finally:
    # Закрываем селектор,
    # чтобы освободить зарегистрированные сокеты и ресурсы.
    # Сам lsock закрывается неявно при завершении процесса,
    # но sel.close() снимает все регистрации корректно.
    sel.close()
