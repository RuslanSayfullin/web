##### _разработка Sayfullin R.R.

Инструкция актуальна для Linux-систем.
========================================================================================================================

Скопируйте репозиторий с помощью команды:
$ git clone https://github.com/RuslanSayfullin/web.git
Перейдите в основную директорию с помощью команды: 
$ cd web

Создать и активировать виртуальное окружение:
========================================================================================================================
$ poetry env use python3.11
Установить зависимости:
$ poetry install 
Сохранить, адрес созданного виртуального окружения из вывода(рекомендуется)
$ poetry shell
(web-py3.11) $
Выход:
$ exit

/home/user/.cache/pypoetry/virtualenvs/

Добавить в директорию web/portal файл psw.py
========================================================================================================================
В данный файл, необходимо добавить две переменные:

secret_key = 'ваш секретный ключ'   # секретный ключ приложения
dbase_psw = 'ваш ключ к БД'         # Пароль для подключения к БД

Создание БД
========================================================================================================================
Войдите в интерактивный сеанс Postgres, набрав:
$ sudo -u postgres psql


=# CREATE DATABASE contracts;
=# CREATE USER portaluser WITH PASSWORD 'myPassword';
=# GRANT ALL PRIVILEGES ON DATABASE contracts TO portaluser;
=# \q
$ exit

Перейти в директорию contracts
========================================================================================================================
Для запуска выполнить следующие команды:
Команда для создания миграций приложения для базы данных
$ python3 manage.py makemigrations
$ python3 manage.py migrate

Создание суперпользователя
$ python3 manage.py createsuperuser

Будут выведены следующие выходные данные. Введите требуемое имя пользователя, электронную почту и пароль:
по умолчанию почта admin@admin.com пароль: 12345

Username (leave blank to use 'admin'): admin
Email address: admin@admin.com
Password: ********
Password (again): ********
Superuser created successfully.

Команды для запуска приложения:
$ python3 manage.py runserver


Django-приложение будет доступно по адресу: http://127.0.0.1:8000/

JSON:

{
  "uuid": "1B",
  "name": "ООО Энергия",
  "address": "fdrshrshsr",
  "phone": "+7(987) 2405-525",
  "owner": 1,
  "type_production": "Кухонный гарнитур"
}

Прочее
------------------------------------------------------------------------------------------------------------------------
$ python3 -m pip freeze > requirements.txt
$ python3 -m pip install -r requirements.txt
$ scp /home/rusl4n/Documents/projects/web/portal/psw.py cryptolis@80.78.244.196:/home/cryptolis/web/portal

http://80.78.244.196:8000
http://80.78.244.196:8000/admin/
gunicorn --bind 0.0.0.0:8000 portal.wsgi

80-78-244-196