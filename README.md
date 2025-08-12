# 🚀 FastAPI Learning Project

Проект для изучения современного Python веб-фреймворка FastAPI с практическими примерами и упражнениями.

## 📋 О проекте

FastAPI — это современный, быстрый веб-фреймворк для создания API с использованием Python, основанный на стандартных подсказках типов Python. Этот проект создан для систематического изучения возможностей FastAPI от базовых концепций до продвинутых техник.

## ✨ Особенности FastAPI

- **Высокая производительность** — один из самых быстрых Python фреймворков
- **Автоматическая документация** — интерактивная документация API (Swagger UI)
- **Проверка типов** — автоматическая валидация данных на основе аннотаций типов
- **Современный Python** — поддержка async/await из коробки
- **Стандарты** — основан на OpenAPI и JSON Schema

## 🎯 Цели обучения

- [ ] Основы создания API endpoints
- [ ] Работа с моделями данных (Pydantic)
- [ ] Валидация и сериализация данных
- [ ] Асинхронное программирование
- [ ] Аутентификация и авторизация
- [ ] Работа с базами данных
- [ ] Тестирование FastAPI приложений
- [ ] Развертывание в production

## 🛠 Технологический стек

- **Python 3.8+**
- **FastAPI** — основной фреймворк
- **Pydantic** — валидация данных
- **SQLAlchemy** — ORM для работы с БД
- **Alembic** — миграции БД
- **PostgreSQL/SQLite** — база данных
- **pytest** — тестирование
- **Docker** — контейнеризация

## 📁 Структура проекта

```
fastapi-learning/
├── app/
│   ├── __init__.py
│   ├── main.py              # Главный файл приложения
│   ├── models/              # Модели данных
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic схемы
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes/              # Маршруты API
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── users.py
│   ├── database/            # Настройки БД
│   │   ├── __init__.py
│   │   └── connection.py
│   └── utils/               # Утилиты
│       ├── __init__.py
│       └── security.py
├── tests/                   # Тесты
│   ├── __init__.py
│   └── test_main.py
├── alembic/                 # Миграции
├── requirements.txt         # Зависимости
├── docker-compose.yml       # Docker конфигурация
├── .env.example            # Пример переменных окружения
└── README.md
```

## 🚀 Быстрый старт

### Установка

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd fastapi-learning
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл
```

### Запуск приложения

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

Интерактивная документация API: http://localhost:8000/docs

## 📚 Модули обучения

### 1. Основы FastAPI
- Создание первого API endpoint
- Параметры пути и запроса
- Тела запросов
- Модели ответов

### 2. Модели данных с Pydantic
- Создание схем данных
- Валидация входных данных
- Сериализация ответов
- Вложенные модели

### 3. Работа с базой данных
- Настройка SQLAlchemy
- Создание моделей
- CRUD операции
- Миграции с Alembic

### 4. Аутентификация и безопасность
- JWT токены
- Хеширование паролей
- Защита endpoints
- OAuth2 схемы

### 5. Продвинутые возможности
- Dependency Injection
- Middleware
- Background Tasks
- WebSockets

### 6. Тестирование
- Модульные тесты
- Интеграционные тесты
- Тестирование с TestClient
- Моки и фикстуры

## 🧪 Примеры кода

### Простой endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

### Pydantic модель

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    is_active: bool = True
```

## 📊 Полезные команды

```bash
# Запуск с автоперезагрузкой
uvicorn app.main:app --reload

# Запуск тестов
pytest

# Создание миграции
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head

# Запуск с Docker
docker-compose up --build
```

## 📖 Дополнительные ресурсы

- [Официальная документация FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic документация](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy документация](https://docs.sqlalchemy.org/)
- [Примеры FastAPI на GitHub](https://github.com/tiangolo/fastapi/tree/master/docs_src)

## 🤝 Участие в проекте

1. Форкните проект
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте ветку (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

## 👨‍💻 Автор

Ваше имя - [email@example.com](mailto:email@example.com)

---

**Счастливого изучения FastAPI! 🎉**