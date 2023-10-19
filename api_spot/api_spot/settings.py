import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True
ALLOWED_HOSTS = (os.getenv('ALLOWED_HOSTS'), 'localhost:9000', '127.0.0.1', '[::1]')


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
    'corsheaders',
    'ckeditor',
    'storages',

    'users',
    'spots',
    'information',
    'api',

    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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



CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost',
#     'http://' + os.getenv('HOST')
# ]

CSRF_TRUSTED_ORIGINS = (
    'http://localhost',
    'https://' + os.getenv('ALLOWED_HOSTS'),
    'http://' + os.getenv('ALLOWED_HOSTS')
    
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

MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
# MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
# MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")

# AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
# AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
AWS_S3_ENDPOINT_URL = 'http://minio:9000'

AWS_S3_USE_SSL = False
AWS_S3_URL_PROTOCOL = 'http:'
AWS_S3_REGION_NAME = 'eu-west-1'

STATIC_URL = 'http://minio/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "http://localhost/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            "bucket_name": 'media',
            "region_name": AWS_S3_REGION_NAME,
            'url_protocol': AWS_S3_URL_PROTOCOL,
            'use_ssl': AWS_S3_USE_SSL,
            'endpoint_url': AWS_S3_ENDPOINT_URL,
            'querystring_auth': False,
            'default_acl': 'public-read',
        }
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'access_key': 'qAgRpNXvgBN8VlNnSUsl',
            'secret_key': 'lnw3QsilEQy0V0Yoe4lq3F2tj8MuSl2WUk5pc99A',
            "bucket_name": 'static',
            "region_name": AWS_S3_REGION_NAME,
            'url_protocol': AWS_S3_URL_PROTOCOL,
            'use_ssl': AWS_S3_USE_SSL,
            'endpoint_url': AWS_S3_ENDPOINT_URL,
            'querystring_auth': False,
            # 'default_acl': 'public-read',
        }
    },
}
