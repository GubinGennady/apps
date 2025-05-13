apps (PlatformForExchangingThings)
=======
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-brightgreen)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue)](https://postgresql.org)

Платформа для бартерного обмена вещами между пользователями. Веб-приложение позволяет:

- 🛠 Создавать/редактировать объявления
- 🔍 Искать товары по категориям и состоянию
- 🤝 Отправлять предложения обмена
- 🔐 Управлять статусами предложений
- 📱 Работать через REST API

## Особенности

✅ **Основной функционал**

- JWT + Session аутентификация
- Пагинация и фильтрация объявлений
- Система обмена с подтверждением
- Кастомная модель пользователя
- Админ-панель Django

🛠 **Технологии**

- Django 5.2
- Django REST Framework
- PostgreSQL
- pytest для тестирования
- Docker-готовность (в разработке)

## Установка

1. **Клонировать репозиторий**
    ```bash
    git clone https://github.com/GubinGennady/apps.git
    cd apps

2. **Создать и активировать виртуальное окружение**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate.bat  # Windows

3. **Установить зависимости**
   ```bash
   pip install -r requirements.txt

4. **Настройка переменного окружения**

   **Создать файл .env в корне проекта:**
   ```ini
   SECRET_KEY=ваш_секретный_ключ
   DEBUG=True
   NAME=postgres
   USER=postgres
   PASSWORD=postgres
   HOST=localhost
   PORT=5432
5. **Настройка БД**

   **Установить PostgreSQL**

   **Создать БД:**
   ```sql
   CREATE DATABASE postgres;
6. **Миграции**
   ```bash
   python manage.py makemigrations  
   python manage.py migrate

## Запуск сервера

    pytest -v     
    pytest ads/tests/test_models.py -v
    pytest ads/tests/test_views.py -v      
    pytest ads/tests/ api/tests/ --ds=config.settings

## Использование API

**Основные эндпоинты:**

    GET    /api/v1/ads/          - список объявлений
    POST   /api/v1/ads/          - создать объявление
    GET    /api/v1/ads/{id}/     - детали объявления
    PUT    /api/v1/ads/{id}/     - обновить объявление
    DELETE /api/v1/ads/{id}/     - удалить объявление
    POST   /api/v1/proposals/    - создать предложение
    PATCH  /api/v1/proposals/{id}/ - обновить статус

**Пример запроса:**

    curl -X GET http://localhost:8000/api/v1/ads/

## Модели данных

👤 Пользователь (CustomUser)

    username
    email
    phone_number
    address

📢 Объявление (Ad)

    user (ForeignKey)
    title
    description
    category (choices)
    condition (choices)
    created_at

🔄 Предложение обмена (ExchangeProposal)

    ad_sender (ForeignKey)
    ad_receiver (ForeignKey)
    status (choices: pending/accepted/rejected)
    created_at

## 📂 Структура проекта

      apps/
      ├── ads/                      # Основное приложение (объявления и обмены)
      │   ├── migrations/           # Миграции базы данных (автогенерируемые)
      │   ├── templates/            # HTML-шаблоны (Django Template Language)
      │   │   ├── ads/
      │   │   │   ├── registration/ # Шаблоны авторизации
      │   │   │   │   ├── login.html
      │   │   │   │   └── register.html
      │   │   │   ├── ad_confirm_delete.html  # Подтверждение удаления
      │   │   │   ├── ad_detail.html          # Детали объявления
      │   │   │   ├── ad_form.html            # Форма создания/редактирования
      │   │   │   ├── ad_list.html            # Список объявлений с фильтрами
      │   │   │   ├── main.html               # Главная страница
      │   │   │   ├── proposal_form.html      # Форма предложения обмена
      │   │   │   └── proposal_update.html    # Обновление статуса предложения
      │   │   └── base.html        # Базовый шаблон (наследование для всех страниц)
      │   ├── tests/               # Тесты приложения
      │   │   ├── __init__.py
      │   │   ├── test_models.py   # Тесты моделей (валидация, методы)
      │   │   └── test_views.py    # Тесты представлений (CRUD, логика)
      │   ├── __init__.py
      │   ├── admin.py             # Регистрация моделей в админке + кастомизация
      │   ├── apps.py              # Конфигурация приложения (class AdsConfig)
      │   ├── forms.py             # Формы Django (AdForm, ExchangeProposalForm)
      │   ├── models.py            # Модели данных (CustomUser, Ad, ExchangeProposal)
      │   ├── urls.py              # Локальные URL-маршруты приложения
      │   └── views.py             # Class-Based Views (AdListView, ProposalCreateView)
      │
      ├── api/                     # REST API приложение (DRF)
      │   ├── __init__.py
      │   ├── apps.py              # Конфигурация API-приложения
      │   ├── serializers.py       # Сериализаторы моделей (Ad, Proposal, User)
      │   ├── urls.py              # Маршруты API (Router для ViewSets)
      │   └── views.py             # ViewSets (AdViewSet, ProposalViewSet)
      │   ├── config/                   # Ядро проекта
      │   │   ├── __init__.py           # Инициализация пакета
      │   │   ├── settings.py           # Основные настройки (БД, middleware, приложения)
      │   │   ├── urls.py               # Главный роутинг URL → включает urls.py приложений
      │   │   └── wsgi.py               # Точка входа для WSGI-серверов (Gunicorn/uWSGI)
      ├── env/                          # Виртуальное окружение (игнорируется)
      ├── static/                  # Статические ресурсы (коллекция через collectstatic)
      │   ├── css/                 # Стили (Bootstrap-кастомизация)
      │   │   ├── bootstrap.min.css
      │   │   └── bootstrap-icons.min.css
      │   └── js/                  # JavaScript-логика (формы, фильтры)
      │       └── bootstrap.bundle.min.js
      │
      ├── .env                     # Конфиденциальные настройки (SECRET_KEY, DB)
      ├── .env.sample              # Шаблон для .env (без реальных значений)
      ├── .gitignore               # Игнорируемые файлы (venv, .env, __pycache__)
      ├── conftest.py              # Глобальные фикстуры pytest (доступ к БД)
      ├── manage.py                # Управление проектом (миграции, запуск)
      ├── pytest.ini               # Конфигурация тестов (настройки Django)
      ├── README.md                # Инструкции (установка, использование, лицензия)
      └── requirements.txt         # Зависимости (Django, DRF, psycopg2, pytest)

## 🆘 Поддержка

При возникновении проблем:

    1. Проверьте логи приложения
    2. Убедитесь в корректности миграций
    3. Для экстренных случаев:
        Email: gubingm@list.ru
        Telegram: @juniormasterpython

