# match_site

## Описание
Сайт предоставляет информацию о результатах игр футбольной Английской Премьер-лиги.
Результаты матчей и турнирная таблица обновляются автоматически, используя Celery. Также присутствует краткая информация о каждом клубе, участвующем в турнире.

![image](https://github.com/AlnBnd/match_site/assets/70378024/069286a6-1fea-47d1-91de-8f59f88a5925)
![image](https://github.com/AlnBnd/match_site/assets/70378024/6eb7e524-981f-448d-940e-95a47aa9253d)

Основные компоненты веб-приложения включают:

- **URL**: Направляют запросы к представлениям (Views).
- **Views**: Обрабатывают данные, взаимодействуя с моделями (Models).
- **Models**: Управляют взаимодействием с базой данных (Database) для сохранения или извлечения данных.
- **Templates**: Используются для формирования HTML-ответов, отправляемых пользователям.
- **Celery Broker**: Координирует передачу асинхронных задач к Celery Worker.
- **Celery Worker**: Выполняет задачи по обновлению данных, включая обращение к внешним API и обновление моделей в базе данных.
![image](https://github.com/AlnBnd/match_site/assets/70378024/7ea92e35-120c-4f9d-a0bb-480dfe20aba6)

## Подробное описание проекта и его функций.
### Технологии
- Python 3.11.5
- Django 5.0.2
- Redis 5.0.2
- Celery 5.3.6

### Установка и настройка
1. Для изоляции зависимостей проекта рекомендуется использовать виртуальное окружение.
```bash
python -m venv venv
```
   Запуск виртуального окружения:

Windows:
```bash
.\djvenv\Scripts\activate
```
Linux\macOS:
```bash
source djvenv/bin/activate
```
2. Клонируйте проект:
```bash
git clone
```
3 Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Для безопасного необходимо SECRET_KEY добавить в `.env` файл, который создаётся в Django проекте. Так же нужно получит API_KEY c сайта https://www.football-data.org, API_KEY нужно добавить в `.env`
```
SECRET_KEY=ваш_секретный_ключ_django
API_KEY=ваш_api_ключ_с_сайта_football_data
```
5. Настройте базу данных и выполните миграции:
```bash
python manage.py migrate
```
  Эта команда создаст необходимые таблицы в базе данных согласно моделям приложений Django.
6. Установка и запуск Redis на локальном устройстве:
```
redis-server
```
7. Запустите сервер разработки:
```bash
python manage.py runserver
```
При каждом запуске сервера информация о матчах будет обновляться автоматически благодаря воркерам Django Celery, запущенным через django-extensions.
