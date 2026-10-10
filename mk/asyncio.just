# =============================================================================
# Asyncio study just commands
# =============================================================================

set working-directory := '..'

path_prefix := 'async_ds'
run_command := 'poetry run python3 -m'

listing-1-2:  # Процессы и потоки в простом Python приложении
    {{run_command}} {{path_prefix}}.book.chapter_01.listing_1_2

listing-1-3:  # Создание многопоточного Пайтон процесса
    {{run_command}} {{path_prefix}}.book.chapter_01.listing_1_3

listing-1-4:  # Создание нескольких процессов
    {{run_command}} {{path_prefix}}.book.chapter_01.listing_1_4

listing-1-5:  # Генерирование последовательности Фибоначи и его хронометраж
    {{run_command}} {{path_prefix}}.book.chapter_01.listing_1_5

listing-2-7:  # Выполнение двух сопрограмм
    {{run_command}} {{path_prefix}}.book.book.chapter_02.listing_2_7

listing-2-8:  # Создание задачи
    {{run_command}} {{path_prefix}}.book.chapter_02.listing_2_8

listing-2-9:  # Конкурентное выполнение нескольких задач
    {{run_command}} {{path_prefix}}.book.chapter_02.listing_2_9

listing-3-1:  # Запуск сервера и прослушивание порта для подключения
    {{run_command}} {{path_prefix}}.book.book.chapter_03.listing_3_1

listing-3-2:  # Чтение данных из сокета
    {{run_command}} {{path_prefix}}.book.chapter_03.listing_3_2

listing-3-3:  # Подключение нескольких клиентов
    {{run_command}} {{path_prefix}}.book.chapter_03.listing_3_3

listing-3-4:  # Создание неблокирующего сервера
    {{run_command}} {{path_prefix}}.book.chapter_03.listing_3_4

listing-3-7:  # Использование селектора для построения неблокирующего сервера
    {{run_command}} {{path_prefix}}.book.chapter_03.listing_3_7


# ================================
# Глава 4 Конкурентные веб-серверы
# ================================

listing-4-1:  # Асинхронный контекстный менеджер, ожидающий подключения клиента
    {{run_command}} {{path_prefix}}.book.chapter_04.listing_4_1

listing-4-2:  # Отправка веб запроса с помощью aiohttp
    {{run_command}} {{path_prefix}}.book.chapter_04.listing_4_2


# =========================================
# Глава 5 Неблокирующие драйверы баз данных
# =========================================

listing-5-1:  # Подключение к postgreSQL
    {{run_command}} {{path_prefix}}.book.chapter_05.listing_01


# =====================
# Глава 8 Потоки данных
# =====================

listing-8-2:  # Использование протокола
    {{run_command}} {{path_prefix}}.book.chapter_08.listing_2

listing-8-12:  # Создание эхо-сервера с помощью серверных объектов
    {{run_command}} {{path_prefix}}.book.chapter_08.listing_12

listing-8-13:  # Запустить чат-сервер
    {{run_command}} {{path_prefix}}.book.chapter_08.listing_13

listing-8-14:  # Запустить клиента чат-сервера
    {{run_command}} {{path_prefix}}.book.chapter_08.listing_14


# ======================
# Глава 9 Веб-приложения
# ======================

listing-9-1:  # Запустить сервер текущего времени
    {{run_command}} {{path_prefix}}.book.chapter_09.listing_01

listing-9-2:  # Подключение к базе данных о товарах
    {{run_command}} {{path_prefix}}.book.chapter_09.listing_02

listing-9-3:  # Подключение к postgreSQL
    {{run_command}} {{path_prefix}}.book.chapter_09.listing_03


# =====================
# Глава 10 Микросервисы
# =====================

listing-10-1:  # Запустить сервис наличия на складе
    {{run_command}} {{path_prefix}}.book.chapter_10.listing_01

listing-10-5:  # Запустить сервис избранного
    {{run_command}} {{path_prefix}}.book.chapter_10.listing_05

listing-10-6:  # Запустить сервис корзины
    {{run_command}} {{path_prefix}}.book.chapter_10.listing_06

# ================
# Asyncio examples
# ================

example-run-server:  # Запустить пример сервера
    {{run_command}} {{path_prefix}}.di.main

example-run-listing-9-9:  # Run Starlatte application (di)
    poetry run uvicorn --workers 1 {{path_prefix}}.di.web.starlatte.main:app

example-run-listing-9-11:
    poetry run gunicorn \
        --pythonpath src/eip/examples/asyncio/di/web/django \
        async_views.asgi:application \
        -k uvicorn.workers.UvicornWorker