"""Создание сногопоточного Пайтон процсса."""

import threading


def hello_from_thread() -> None:
    """Print current thread representation."""
    print(f'Привет от потока {threading.current_thread()}!')


hello_thread = threading.Thread(target=hello_from_thread)
hello_thread.start()

total_threads = threading.active_count()
thread_name = threading.current_thread().name

print(f'В данный момент Пайтон исполняет {total_threads} поток(ов)')
print(f'Имя текущего потока {thread_name}')
hello_thread.join()


# Дополнение к листингу

print(f'Имя дочернего потока {hello_thread.name}')
