"""Запуск сервера и прослушивание порта для подключения."""

import socket

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST, PORT)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(ADDR)
server_socket.listen()

connection, client_address = server_socket.accept()
print(f'Получен запрос на подключение от {client_address}!')
