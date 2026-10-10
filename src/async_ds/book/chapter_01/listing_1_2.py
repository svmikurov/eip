"""Процессы и потоки в простом Python приложении.

Листинг 1.2
"""

import os
import threading

print(f'Исполняется Пайтон-процесс с идентификатором: {os.getpid()}')

total_threads = threading.active_count()
thread_name = threading.current_thread().name

print(f'В данный момент Пайтон исполняет {total_threads} поток(ов)')
print(f'Имя текущего потока {thread_name}')


# Дополнение к листингу

native_id = threading.current_thread().native_id
print(
    f'Исполняется поток идентификатором от ОС (Linux TID): {native_id},\n'
    f'его номер соответствует Пайтон-процессу, так-как поток один'
)
