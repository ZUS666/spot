import pytest


@pytest.fixture(autouse=True)
def use_dummy_cache_backend(settings, redis_proc):
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': f'redis://{redis_proc.host}:{redis_proc.port}/1',
        }
    }

# может не завершиться процесс, после режима дебаг kill $(lsof -i:6379)


@pytest.fixture(scope='session')
def celery_config(redis_proc):
    return {
        'broker_url': f'redis://{redis_proc.host}:{redis_proc.port}/0',
        'result_backend': f'redis://{redis_proc.host}:{redis_proc.port}'
    }


@pytest.fixture(scope='session')
def celery_includes():
    return [
        'api_spot.celery',
    ]
