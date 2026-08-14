# File Server

Приложение для загрузки файлов на сервер.
Дипломный проект SkyPro (TF2).

## Функциональность

- Регистрация и авторизация (JWT)
- Загрузка файлов
- Проверка дубликатов
- Публичные ссылки для общего доступа
- Отправка отчётов на email
- Статистика загрузок
- Профиль пользователя

## Тэги

- CORS
- Git
- ORM
- OpenAPI Docs
- PEP8
- PostgreSQL
- Readme
- Serialiers
- Test
- Viewset/Generic
- Docker
- Docker-Compose
- Права доступа

## Запуск

1. Скопируйте `.env.example` в `.env` и заполните переменные.
2. `docker compose up --build -d`
3. `docker compose exec web python manage.py migrate`
4. `docker compose exec web python manage.py createsuperuser`
5. Откройте `http://localhost:8000`

## Эндпоинты API

- `/api/auth/register/` — регистрация
- `/api/auth/token/` — получение JWT
- `/api/auth/user/` — профиль
- `/api/files/` — CRUD файлов
- `/api/files/{id}/download/` — скачивание
- `/api/stats/` — статистика
- `/swagger/` — документация

## Автор

Цой Алексей, 2026