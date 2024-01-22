# Документация приложения

## Общее описание

Это приложение - бот для Telegram, который помогает пользователям получать информацию о магазинах и товарах. Он использует MongoDB для хранения данных и библиотеку `telebot` для взаимодействия с API Telegram.

## Структура приложения

Приложение состоит из следующих модулей:

1. `main.py`: Главный модуль, который запускает бота и обрабатывает команды пользователя.
2. `user_interface.py`: Модуль, отвечающий за взаимодействие с пользователем. Он формирует сообщения, которые отправляются пользователю.
3. `database_handler.py`: Модуль, отвечающий за взаимодействие с базой данных MongoDB. Он получает данные о магазинах и товарах из базы данных.
4. `config.py`: Модуль, содержащий конфигурационные данные, такие как токен бота и параметры подключения к базе данных.

## Структура базы данных

База данных MongoDB используется для хранения данных о магазинах и товарах. Она имеет следующую структуру:

- База данных: `e-commerce`
- Коллекция: `products`
- Документы: Каждый документ содержит массив `shops`, который содержит объекты магазинов. Каждый магазин имеет следующие поля:
    - `name`: Название магазина.
    - `website`: Веб-сайт магазина.
    - `description`: Описание магазина.
    - `locations`: Массив объектов, представляющих различные местоположения магазина. Каждое местоположение имеет поля `city`, `address`, `working_hours` и `name`.
    - `products`: Массив объектов, представляющих товары, доступные в магазине. Каждый товар имеет поля `name` и `image_url`.

## Функции

Вот некоторые ключевые функции в приложении:

- `set_bot(b)`: Устанавливает глобальную переменную `bot` в `user_interface.py`.
- `ask_for_shop(message)`: Запрашивает у пользователя название магазина.
- `process_shop_step(message)`: Обрабатывает ответ пользователя на запрос названия магазина.
- `send_shop_info(message, shop_name)`: Отправляет подробную информацию о магазине пользователю.
- `send_all_shops(bot, message)`: Отправляет краткую информацию обо всех магазинах пользователю.
- `send_products_in_shop(bot, message, shop_name)`: Отправляет список товаров, доступных в указанном магазине, пользователю.
- `send_shops_by_brand(bot, message, brand_name)`: Отправляет все магазины определённого бренда пользователю.
- `get_shop_info(shop_name)`: Возвращает подробную информацию о магазине по его имени.
- `get_all_shops()`: Возвращает краткую информацию обо всех магазинах.

## Запуск приложения

Для запуска приложения выполните следующие шаги:

1. Установите необходимые зависимости, используя pip: `pip install -r requirements.txt`
2. Запустите `main.py`: `python main.py`
