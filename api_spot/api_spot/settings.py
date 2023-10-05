import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = (os.getenv('ALLOWED_HOSTS'), )

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'djoser',
    'phonenumber_field',
    'drf_spectacular',
    'gmailapi_backend',
    'django_celery_beat',

    'users',
    'spots',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_spot.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (TEMPLATES_DIR, ),
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

WSGI_APPLICATION = 'api_spot.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": os.getenv('DB_ENGINE'),
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('POSTGRES_USER'),
        "PASSWORD": os.getenv('POSTGRES_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CSRF_TRUSTED_ORIGINS = (
    'http://localhost',
    os.getenv('CRSF_HOST')
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.user'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API SPOT',
    'DESCRIPTION': 'Апи для коворкинког',
    'VERSION': '0.0.5',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': r'/api/v1',
}

TIMEOUT_CACHED_CODE = 10 * 60
TIMEOUT_CACHED_COUNTER = 6 * 60 * 60
TIMEOUT_CACHED_RATING = 5 * 60
TIMEOUT_CACHED_LOW_PRICE = 5 * 60

TIME_CHANGE_STATUS = 60 * 10
LEN_CONFIRMATION_CODE = 6

COMPANY_NAME = os.getenv('COMPANY_NAME')

EMAIL_BACKEND = 'gmailapi_backend.mail.GmailBackend'

GMAIL_API_CLIENT_ID = os.getenv('GMAIL_API_CLIENT_ID')
GMAIL_API_CLIENT_SECRET = os.getenv('GMAIL_API_CLIENT_SECRET')
GMAIL_API_REFRESH_TOKEN = os.getenv('GMAIL_API_REFRESH_TOKEN')

CELERY_BROKER_URL = os.getenv('CELERY_BROKER')
CELERY_RESULT_BACKEND = os.getenv('CELERY_BROKER')
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_TASK_TRACK_STARTED = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_ADDRESS'),
    }
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'},
    },
}
