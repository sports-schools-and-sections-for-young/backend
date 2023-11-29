## СпортХаб - платформа для объединения спортивных школ и секций для молодежи

http://sporthub.acceleratorpracticum.ru/

http://185.41.162.249/

[![SportHub workflow](https://github.com/sports-schools-and-sections-for-young/backend/actions/workflows/main.yml/badge.svg)](https://github.com/sports-schools-and-sections-for-young/backend/actions/workflows/main.yml)

### 1. Запуск проекта в контейнерах на удаленном сервере

1. Зайти на удаленный сервер и создать папку sport_hub.

2. В папке sport_hub создать файл .env. Пример заполнения файла:
```
SECRET_KEY='KEY'
DEBUG=True # True отладка включена, False отладка отключена
DATABASE=Dev # Prod для PostgreSQL, Dev для SQLite3
POSTGRES_DB=django
POSTGRES_USER=django_user
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=185.41.162.249;127.0.0.1;localhost;sporthub.acceleratorpracticum.ru
CSRF_TRUSTED_ORIGINS=https://sporthub.acceleratorpracticum.ru
SU_NAME=admin
SU_EMAIL=admin@mail.ru
SU_PASSWORD=pass
```
Сгенерировать секретный ключ и сохранить в переменной SECRET_KEY.\
SU_NAME, SU_EMAIL, SU_PASSWORD - данные суперпользователя.\
В переменную ALLOWED_HOSTS записать IP-адрес сервера и доменное имя сайта.
В переменную CSRF_TRUSTED_ORIGINS записать доменное имя сайта.

3. В папку sport_hub скопировать файлы docker-compose.yml и nginx.conf из проекта.

4. На удаленном сервере изменить файл конфигурации Nginx:
```
sudo nano /etc/nginx/sites-enabled/default
```

5. Для этого записать и сохранить новые настройки:
```
server {
    listen 80;
    server_tokens off;
    server_name 185.41.162.249 sporthub.acceleratorpracticum.ru;
    client_max_body_size 20M;
    
    location / {
        proxy_set_header        Host $http_host;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

6. Проверить файл конфигурации Nginx при помощи команды:
```
sudo nginx -t
```

7. Перезагрузить Nginx:
```
sudo systemctl reload nginx
```

8. Запустить проект при помощи команды:
```
sudo docker compose up -d
```

9. Создать и применить миграции к БД:
```
sudo docker compose exec backend python manage.py makemigrations
sudo docker compose exec backend python manage.py migrate
```

10. Собрать статику:
```
sudo docker compose exec backend python manage.py collectstatic --no-input
```

11. Создать суперпользователя:
```
sudo docker compose exec backend python manage.py create_su
```

### 2. Локальный запуск backend

1. Клонировать репозиторий и перейти в папку с проектом.

2. В корне проекта создать файл .env. Пример заполнения файла:

```
SECRET_KEY='KEY'
DEBUG=True # True отладка включена, False отладка отключена
DATABASE=Dev # Prod для PostgreSQL, Dev для SQLite3
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_password
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1;localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1;http://localhost
SU_NAME=admin
SU_EMAIL=admin@mail.ru
SU_PASSWORD=pass
```
Сгенерировать секретный ключ и сохранить в переменной SECRET_KEY.\
SU_NAME, SU_EMAIL, SU_PASSWORD - данные суперпользователя.

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

6. Создать суперпользователя:
```
python manage.py create_su
```

7. Запустить сервер:
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
