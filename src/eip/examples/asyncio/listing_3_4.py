"""Создание неблокирующего сервера."""

import socket

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST, PORT)

BUFFER_SIZE = 2
BACKLOG = 5


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(ADDR)
server_socket.listen()
server_socket.setblocking(False)


connections: list[socket.socket] = []

try:
    while True:
        connection, client_address = server_socket.accept()
        connection.setblocking(False)
        print(f'Получен запрос на подключение от {client_address}!')
        connections.append(connection)

        for connection in connections:
            buffer = b''

            while buffer[-2:] != b'\r\n':
                chunk = connection.recv(BUFFER_SIZE)

                if not chunk:
                    break
                else:
                    print(f'Получена часть данных: {chunk!r}')
                    buffer += chunk

            print(f'Все данные: {buffer!r}')

            connection.sendall(buffer)

finally:
    print('Закрываем сокет сервера')
    server_socket.close()
