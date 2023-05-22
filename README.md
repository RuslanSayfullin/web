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
https://chiffre.tech/

80-78-244-196
15052023reforma

sudo su - postgres 
pg_dump -U postgres contracts > /home/rusl4n/Documents/projects/web/150523.pg_dump

pg_dump -U postgres contracts > /home/rusl4n/Downloads/postgres-dump-directory/160523.pg_dump


server {
        server_name portal-re-formaufa.ru;
        listen portal-re-formaufa.ru:80;
        server_tokens off;
        location /.well-known {
                root /home/portal/web/;
                autoindex off;
                access_log off;
                try_files $uri =404;
        }
        location / {
                return 301 https://$server_name$request_uri;
        }
}
server {
        server_name portal-re-formaufa.ru;
        listen 443 ssl http2;
        ssl_certificate /etc/letsencrypt/live/portal-re-formaufa.ru/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/portal-re-formaufa.ru/privkey.pem;
        ssl_trusted_certificate /etc/letsencrypt/live/portal-re-formaufa.ru/chain.pem;
        ssl_stapling on;
        ssl_stapling_verify on;
        root /home/portal/web;
        index index.php index.html index.htm;
        access_log /home/portal/nginx_logs/portal.log combined;
        error_log /home/portal/nginx_logs/portal.error.log error;
        location / {
                location /static/ {
                        root /home/portal/web/;
                        autoindex off;
                        access_log off;
                }
                location /media/ {
                        root /home/portal/web/;
                        autoindex off;
                }
                location ~* ^.+\.(jpeg|jpg|png|gif|bmp|ico|svg|css|js)$ {
                        expires max;
                        add_header Content-Disposition "attachment";
                        add_header Content-Type "application/force-download";
                        add_header Content-Type "application/octet-stream";
                }
                location ~ [^/]\.php(/|$) {
                        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                        if (!-f $document_root$fastcgi_script_name) {
                                return 404;
                        }
                        fastcgi_pass unix:/run/php/php7.2-fpm.sock;
                        fastcgi_index index.php;
                        include /etc/nginx/fastcgi_params;
                }
                location /.well-known/ {
                        root /home/portal/web/;
                        autoindex off;
                        access_log off;
                }
                location / {
                        include uwsgi_params;
                        proxy_pass http://unix:/home/portal/web/portal.sock;
                        proxy_connect_timeout 120;
                        proxy_send_timeout 150;
                        proxy_read_timeout 600; # 200
                        uwsgi_read_timeout 1800;
                }
        }
         error_page 403 /error/404.html;
        error_page 404 /error/404.html;
        error_page 500 502 503 504 /error/50x.html;
        location /error/ {
                alias /home/portal/nginx_html_document_errors/;
        }
}



[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=portal
Group=www-data
WorkingDirectory=/home/portal/web/
ExecStart=/home/portal/venv_python37/bin/gunicorn --access-logfile /home/portal/gunicorn_logs/access.log --error-logfile /home/portal/gunicorn_logs/error.log --workers 15 --timeout 600 --bind unix:/home/portal/web/portal.sock porta$

[Install]
WantedBy=multi-user.target

