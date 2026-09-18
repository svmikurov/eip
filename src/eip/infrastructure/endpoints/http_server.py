"""Simple HTTP socket server."""

import socket
import random

HOST, PORT = "0.0.0.0", 8000

def handle_client(conn):
    try:
        # Читаем запрос до конца заголовков
        data = b""
        while b"\r\n\r\n" not in data:
            chunk = conn.recv(4096)
            if not chunk:
                return
            data += chunk

        request_line = data.split(b"\r\n", 1)[0].decode(errors="ignore")
        print("Запрос:", request_line)

        # Простейший роутинг: GET / или GET /echo
        number = random.randint(1, 1000)
        body = f"Случайное число: {number}\n".encode("utf-8")

        response = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/plain; charset=utf-8\r\n"
            b"Content-Length: " + str(len(body)).encode() + b"\r\n"
            b"Connection: close\r\n"
            b"\r\n"
            + body
        )
        conn.sendall(response)
    finally:
        conn.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"Сервер слушает http://{HOST}:{PORT}")
    while True:
        conn, addr = sock.accept()
        handle_client(conn)

if __name__ == "__main__":
    main()