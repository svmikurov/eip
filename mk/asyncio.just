# =============================================================================
# Asuncio study just commands
# =============================================================================

set working-directory := '..'

listing-1-2:  # Процессы и потоки в простом Python приложении
    python3 src/eip/examples/asyncio/chapter_01/listing_1_2.py

listing-1-3:  # Создание многопоточного Пайтон процсса
    python3 src/eip/examples/asyncio/chapter_01/listing_1_3.py

listing-1-4:  # Создание нескольких процессов
    python3 src/eip/examples/asyncio/chapter_01/listing_1_4.py

listing-1-5:  # Гененрирование последовательности Фибоначи и его хронометраж
    python3 src/eip/examples/asyncio/chapter_01/listing_1_5.py

listing-2-7:  # Выполнение двух сопрограмм
    python3 src/eip/examples/asyncio/chapter_02/listing_2_7.py

listing-2-8:  # Создание задачи
    python3 src/eip/examples/asyncio/chapter_02/listing_2_8.py

listing-2-9:  # Конкурентное выполнение нескольких задач
    python3 src/eip/examples/asyncio/chapter_02/listing_2_9.py

listing-3-1:  # Запуск сервера и прослушивание порта для подключения
    poetry run python3 src/eip/examples/asyncio/chapter_03/listing_3_1.py

listing-3-2:  # Чтение данных из сокета
    poetry run python3 src/eip/examples/asyncio/chapter_03/listing_3_2.py

listing-3-3:  # Подключение нескольких клиентов
    poetry run python3 src/eip/examples/asyncio/chapter_03/listing_3_3.py

listing-3-4:  # Создание неблокирующего сервера
    poetry run python3 src/eip/examples/asyncio/chapter_03/listing_3_4.py

listing-3-7:  # Использование селектора для построения неблокирующего сервера
    poetry run python3 src/eip/examples/asyncio/chapter_03/listing_3_7.py


# ================================
# Глава 4 Конкурентные веб-серверы
# ================================

listing-4-1:  # Асинхронный контекстный менеджер, ожидающий подключения клиента
    poetry run python3 src/eip/examples/asyncio/chapter_04/listing_4_1.py

listing-4-2:  # Отправка веб запроса с помощью aiohttp
    poetry run python3 src/eip/examples/asyncio/chapter_04/listing_4_2.py


# =====================
# Глава 8 Потоки данных
# =====================

listing-8-2:  # Использование протокола
    poetry run python3 src/eip/examples/asyncio/chapter_08/listing_2.py

listing-8-12:  # Создание эхо-сервера с помощью серверных объектов
    poetry run python3 src/eip/examples/asyncio/chapter_08/listing_12.py

listing-8-13:  # Запустить чат-сервер
    poetry run python3 src/eip/examples/asyncio/chapter_08/listing_13.py

listing-8-14:  # Запустить клиента чат-сервера
    poetry run python3 src/eip/examples/asyncio/chapter_08/listing_14.py


# ======================
# Глава 9 Веб-приложения
# ======================

listing-9-1:  # Запустить сервер текущего времени
    poetry run python3 src/eip/examples/asyncio/chapter_09/listing_01.py
