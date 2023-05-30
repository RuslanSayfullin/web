import os
from pathlib import Path

from portal.psw import secret_key, client_id, client_secret  # импорт секретного ключа
from .settings_db import DATABASES      # импорт данных для "базы данных"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '80.78.244.196', 'chiffre.tech', 'localhost']
# кортеж с перечнем IP-адресов, с которых может вестись разработка.
INTERNAL_IPS = ('127.0.0.1', '80.78.244.196', 'chiffre.tech', 'localhost')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'debug_toolbar',
    'drf_yasg',  # Необходим для  swagger
] + [
    'apps',
    'apps.api',
    'apps.froze',
    'apps.oauth2mailru',
    'apps.search',
    'apps.dogovora',

]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Набор панелей, появляющихся на странице в режиме отладки
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'portal.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portal.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_TZ = True


# "Поисковики" статики. Ищет статику в STATICFILES_DIRS.
STATIC_URL = '/static/'    # URL для шаблонов
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATIC_ROOT = "/home/cryptolis/web/static/"

# Абсолютный путь в файловой системе, с каталогом, где файлы, загруженные пользователями.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Для авторизаций и аутентификаций
LOGIN_URL = 'auth:login'
LOGIN_REDIRECT_URL = 'auth:logout'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'apps.oauth2mailru.backends.MailRuBackend',
)

OAUTH_MAIL_RU_CLIENT_ID = client_id
OAUTH_MAIL_RU_CLIENT_SECRET = client_secret
OAUTH_MAIL_RU_REDIRECT_URI = 'http://portal-re-formaufa.ru/auth/mailru/'

LOGO_NAME = "Ре-Форма"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


