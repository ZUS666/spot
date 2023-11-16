import pytest


@pytest.fixture(scope='session')
def celery_includes():
    return [
        'api_spot.celery',
    ]
