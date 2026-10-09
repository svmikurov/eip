# =============================================================================
# Asyncio study just commands
# =============================================================================

set working-directory := '..'

listing-1-2:  # Процессы и потоки в простом Python приложении
    poetry run python3 -m eip.examples.asyncio.chapter_01.listing_1_2

listing-1-3:  # Создание многопоточного Пайтон процесса
    poetry run python3 -m eip.examples.asyncio.chapter_01.listing_1_3

listing-1-4:  # Создание нескольких процессов
    poetry run python3 -m eip.examples.asyncio.chapter_01.listing_1_4

listing-1-5:  # Генерирование последовательности Фибоначи и его хронометраж
    poetry run python3 -m eip.examples.asyncio.chapter_01.listing_1_5

listing-2-7:  # Выполнение двух сопрограмм
    poetry run python3 -m eip.examples.asyncio.chapter_02.listing_2_7

listing-2-8:  # Создание задачи
    poetry run python3 -m eip.examples.asyncio.chapter_02.listing_2_8

listing-2-9:  # Конкурентное выполнение нескольких задач
    poetry run python3 -m eip.examples.asyncio.chapter_02.listing_2_9

listing-3-1:  # Запуск сервера и прослушивание порта для подключения
    poetry run python3 -m eip.examples.asyncio.chapter_03.listing_3_1

listing-3-2:  # Чтение данных из сокета
    poetry run python3 -m eip.examples.asyncio.chapter_03.listing_3_2

listing-3-3:  # Подключение нескольких клиентов
    poetry run python3 -m eip.examples.asyncio.chapter_03.listing_3_3

listing-3-4:  # Создание неблокирующего сервера
    poetry run python3 -m eip.examples.asyncio.chapter_03.listing_3_4

listing-3-7:  # Использование селектора для построения неблокирующего сервера
    poetry run python3 -m eip.examples.asyncio.chapter_03.listing_3_7


# ================================
# Глава 4 Конкурентные веб-серверы
# ================================

listing-4-1:  # Асинхронный контекстный менеджер, ожидающий подключения клиента
    poetry run python3 -m eip.examples.asyncio.chapter_04.listing_4_1

listing-4-2:  # Отправка веб запроса с помощью aiohttp
    poetry run python3 -m eip.examples.asyncio.chapter_04.listing_4_2


# =========================================
# Глава 5 Неблокирующие драйверы баз данных
# =========================================

listing-5-1:  # Подключение к postgreSQL
    poetry run python3 -m eip.examples.asyncio.chapter_05.listing_01


# =====================
# Глава 8 Потоки данных
# =====================

listing-8-2:  # Использование протокола
    poetry run python3 -m eip.examples.asyncio.chapter_08.listing_2

listing-8-12:  # Создание эхо-сервера с помощью серверных объектов
    poetry run python3 -m eip.examples.asyncio.chapter_08.listing_12

listing-8-13:  # Запустить чат-сервер
    poetry run python3 -m eip.examples.asyncio.chapter_08.listing_13

listing-8-14:  # Запустить клиента чат-сервера
    poetry run python3 -m eip.examples.asyncio.chapter_08.listing_14


# ======================
# Глава 9 Веб-приложения
# ======================

listing-9-1:  # Запустить сервер текущего времени
    poetry run python3 -m eip.examples.asyncio.chapter_09.listing_01

listing-9-2:  # Подключение к базе данных о товарах
    poetry run python3 -m eip.examples.asyncio.chapter_09.listing_02

listing-9-3:  # Подключение к postgreSQL
    poetry run python3 -m eip.examples.asyncio.chapter_09.listing_03


# =====================
# Глава 10 Микросервисы
# =====================

listing-10-1:  # Запустить сервис наличия на складе
    poetry run python3 src/eip/examples/asyncio/chapter_10/listing_01.py

listing-10-5:  # Запустить сервис избранного
    poetry run python3 -m eip.examples.asyncio.chapter_10.listing_05

# ================
# Asyncio examples
# ================

example-run-server:  # Запустить пример сервера
    poetry run python3 -m eip.examples.asyncio.di.main

example-run-listing-9-9:  # Run Starlatte application (di)
    poetry run uvicorn --workers 1 eip.examples.asyncio.di.web.starlatte.main:app

example-run-listing-9-11:
    poetry run gunicorn \
        --pythonpath src/eip/examples/asyncio/di/web/django \
        async_views.asgi:application \
        -k uvicorn.workers.UvicornWorker