import datetime

import pytest


@pytest.fixture
def default_user(django_user_model):
    return django_user_model.objects.create_user(
        email='testuser@gmail.fake',
        password='pass@PASS1',
        first_name='first',
        last_name='last',
    )


@pytest.fixture
def authed_user_client(default_user, create_drf_client):
    return create_drf_client(default_user)


@pytest.fixture
def full_data_user(django_user_model):
    return django_user_model.objects.create_user(
        email='fulldata@gmail.fake',
        password='pass@PASS1',
        first_name='first',
        last_name='last',
        phone='+79220011223',
        birth_date=datetime.date(2000, 2, 2),
        occupation='string',
    )


@pytest.fixture
def full_data_user_client(full_data_user, create_drf_client):
    return create_drf_client(full_data_user)
