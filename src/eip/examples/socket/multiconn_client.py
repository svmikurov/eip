"""Multi-connection socket client."""

import selectors
import socket
import sys
from dataclasses import dataclass, field
from typing import cast

from eip.examples.socket import conf

sel = selectors.DefaultSelector()
messages = [b'Message 1 from client.', b'Message 2 from client.']


@dataclass
class ClientData:
    """Client connection data."""

    conn_id: int
    msg_total: int
    recv_total: int = 0
    messages: list[bytes] = field(default_factory=list)
    outb: bytes = b''


def start_connections(host: str, port: int, num_conns: int) -> None:
    """Open num_conns connections to (host, port).

    host : str
        Server host name or IP address.
    port : int
        Server port number.
    num_conns : int
        How many client connections to open.
    """
    server_addr = (host, port)

    for conn_id in range(1, num_conns + 1):
        print(f'Starting connection {conn_id} to {server_addr}')

        # Сокет делаем неблокирующим, чтобы connect_ex()
        # не блокировал главный цикл. connect_ex() не
        # бросает исключение при ошибке — возвращает код;
        # готовность соединения отслеживается через
        # EVENT_WRITE в селекторе.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)

        # Данные, привязанные к сокету:
        #   connid      — номер соединения (для логов)
        #   msg_total   — сколько всего байт ждём от сервера
        #   recv_total  — сколько уже принято
        #   messages    — копия очереди сообщений на отправку
        #   outb        — буфер байтов, ожидающих отправки
        #
        # messages копируется (copy()), иначе pop(0)
        # в одном соединении опустошит список для остальных.
        # outb — bytes (b""), под sock.send().
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        data = ClientData(
            conn_id=conn_id,
            msg_total=sum(len(message) for message in messages),
            messages=messages.copy(),
        )

        sel.register(sock, events, data=data)


def service_connection(key: selectors.SelectorKey, mask: int) -> None:
    """Service a connection that is ready for I/O.

    key : selectors.SelectorKey
        fileobj - the registered socket
        data    - SimpleNamespace with connid, msg_total,
                  recv_total, messages, outb
    mask : int
        Bitmask of ready events (EVENT_READ, EVENT_WRITE).
    """
    # key.fileobj типизирован как FileObject (сокет, файл,
    # pipe и т.п.). Для клиентского соединения это всегда
    # socket — сужаем тип через cast, чтобы mypy разрешил
    # sock.recv()/sock.send().
    conn = cast(socket.socket, key.fileobj)
    data: ClientData = key.data

    if mask & selectors.EVENT_READ:
        recv_data: bytes = conn.recv(
            conf.MAX_MESSAGE_LEN
        )  # Сокет готов к чтению

        if recv_data:
            print(f'Received {recv_data!r} from connection {data.conn_id}')
            data.recv_total += len(recv_data)

        # Соединение закрываем в двух случаях:
        #   1. recv_data пуст (b"") — сервер закрыл сокет;
        #   2. приняли ровно столько байт, сколько отправили
        #      (recv_total == msg_total) — эхо вернуло всё.
        # Проверка вне if recv_data, т.к. закрыть нужно и
        # когда данные пришли, и когда их нет.
        if not recv_data or data.recv_total == data.msg_total:
            print(f'Closing connection {data.conn_id}')
            sel.unregister(conn)
            conn.close()

    if mask & selectors.EVENT_WRITE:
        # Если буфер отправки пуст, берём следующее
        # сообщение из очереди. pop(0) удаляет его из
        # списка, чтобы не отправить повторно.
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)

        if data.outb:
            print(f'Sending {data.outb!r} to connection {data.conn_id}')

            # send() может отправить меньше, чем лежит
            # в буфере (например, если буфер отправки
            # сокета заполнен), поэтому ориентируемся
            # на возвращённое число байт.
            sent = conn.send(data.outb)  # Сокет готов к записи

            # Удаляем из буфера уже отправленные байты;
            # остаток будет отправлен при следующем EVENT_WRITE.
            data.outb = data.outb[sent:]


def main() -> None:
    """Send messages."""
    if len(sys.argv) != 4:
        print(f'Usage: {sys.argv[0]} <host> <port> <num_connections>')
        sys.exit(1)

    host, port, num_conns = sys.argv[1:4]
    start_connections(host, int(port), int(num_conns))

    try:
        while True:
            # select() с timeout=1 (а не None, как в сервере)
            # нужен, чтобы периодически проверять, остались ли
            # зарегистрированные сокеты, и выйти, когда все
            # соединения закрыты. С timeout=None цикл висел бы
            # вечно после закрытия последнего соединения.
            events = sel.select(timeout=1)
            if events:
                for key, mask in events:
                    service_connection(key, mask)

            # Если в селекторе не осталось ни одного сокета —
            # все соединения закрыты, дальше ждать нечего.
            if not sel.get_map():
                break

    except KeyboardInterrupt:
        print('Caught keyboard interrupt, exiting')

    except ConnectionRefusedError:
        print(
            f'Connection refused: server not running on {host}:{port}, exiting'
        )

    finally:
        # Освобождаем ресурсы селектора
        # (снимает все регистрации сокетов).
        sel.close()


if __name__ == '__main__':
    main()
