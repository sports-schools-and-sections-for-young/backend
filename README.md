## СпортХаб - платформа для объединения спортивных школ и секций для молодежи

***

[![SportHub workflow](https://github.com/sports-schools-and-sections-for-young/backend/actions/workflows/main.yml/badge.svg)](https://github.com/sports-schools-and-sections-for-young/backend/actions/workflows/main.yml)

### 1. Локальный запуск приложения

1. Клонировать репозиторий и перейти в папку с проектом.
2. В корне проекта создать файл .env. Пример заполнения файла:

```
SECRET_KEY='KEY'
DEBUG=True # True отладка включена, False отладка отключена
DATABASE=Dev # Prod для PostgreSQL, Dev для SQLite3
POSTGRES_DB=django
POSTGRES_USER=django_user
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1;localhost
```
Сгенерировать секретный ключ и сохранить в переменной SECRET_KEY

3. Для запуска приложения, необходимо перейти в папку backend, создать и активировать виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```

4. Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

5. Создать и применить миграции к БД:
```
python manage.py makemigrations
python manage.py migrate
```

6. Запустить сервер:
```
python manage.py runserver
```
Проект доступен по адресу http://127.0.0.1:8000/

Swagger http://127.0.0.1:8000/api/swagger/

ReDoc http://127.0.0.1:8000/api/redoc/

Админка http://127.0.0.1:8000/admin/

Доступны два эндпойнта:
- поиск секций по фильтрам http://127.0.0.1:8000/api/search_sections/
- отображение всех видов спорта http://127.0.0.1:8000/api/sport_types/

### 2. Локальный запуск приложения в контейнерах

---ЭТО БУДЕТ ПОТОМ---
