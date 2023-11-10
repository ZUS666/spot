import datetime

import pytest
from django.core.cache import cache
from rest_framework import status


@pytest.mark.django_db
class TestUserRegistration:
    """
    Тесты регистрации пользователя.
    """
    url_signup = '/api/v1/users/'
    url_activation = '/api/v1/users/activation/'
    url_resend_confirmation_code = '/api/v1/users/resend_confirmation_code/'
    data = {
        'email': 'valid@mail.fake',
        'first_name': 'fakefn',
        'last_name': 'fakeln',
        'password': 'asd@QWE123',
        're_password': 'asd@QWE123',
    }

    def test_invalid_data_signup(self, unauthed_client):
        """
        Тесты регистрации с невалидными данными.
        """
        invalid_data_fields = (
            ('email', 'asd',),
            ('first_name', 'a1',),
            ('first_name', '.aa',),
            ('first_name', 'a%',),
            ('password', 'asd',),
            ('re_password', 'asd@ASD321',),
        )
        for field, value in invalid_data_fields:
            invalid_data = self.data.copy()
            invalid_data[field] = value
            response = unauthed_client.post(self.url_signup, data=invalid_data)
            assert response.status_code == status.HTTP_400_BAD_REQUEST, (
                f'{self.url_signup} {response.status_code}'
                f'with {field} {value}'
            )

    def test_valid_data_signup(self, unauthed_client, django_user_model):
        """
        Тестирование регистрации пользователя.
        """
        assert django_user_model.objects.count() == 0
        response = unauthed_client.post(self.url_signup, data=self.data)
        assert response.status_code == status.HTTP_201_CREATED, (
            f'{self.url_signup} {response.status_code}'
            f'with data:{self.data}'
        )
        assert django_user_model.objects.count() == 1
        first_user = django_user_model.objects.get(id=1)
        assert first_user.is_active is False
        response = unauthed_client.post(self.url_signup, data=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f'{self.url_signup} {response.status_code}'
            'with exists email'
        )
        data_resend = {
            'email': self.data['email']
        }
        response = unauthed_client.post(
            self.url_resend_confirmation_code,
            data=data_resend,
        )
        assert response.status_code == status.HTTP_200_OK, (
            f'{self.url_signup} {response.status_code}'
            'resend code to user.is_active=False'
        )
        confirmation_code = cache.get(first_user.id)
        activation_data = (
            ('example@mail.com', confirmation_code,
             status.HTTP_400_BAD_REQUEST),
            (first_user.email, '123321', status.HTTP_400_BAD_REQUEST),
            (first_user.email, confirmation_code, status.HTTP_200_OK),
            (first_user.email, confirmation_code, status.HTTP_400_BAD_REQUEST),
        )
        for email, confirmation_code, status_code in activation_data:
            data = {
                'email': email,
                'confirmation_code': confirmation_code
            }
            response = unauthed_client.post(self.url_activation, data=data)
            assert response.status_code == status_code, (
                f'{self.url_signup} {response.status_code}'
                f'{email} {confirmation_code}'
                f'expected status code = {status_code}'
            )
        first_user.refresh_from_db()
        assert first_user.is_active is True


@pytest.mark.django_db
class TestUserActions:
    url_change_password = '/api/v1/users/change_password/'
    url_me = '/api/v1/users/me/'
    url_reset_password_code = '/api/v1/users/reset_password_confirmation_code/'
    url_resend_password_code = '/api/v1/users/resend_confirmation_code/'
    url_reset_password = '/api/v1/users/reset_password/'

    def test_user_change_password(
        self,
        authed_user_client,
        unauthed_client,
    ):
        response = unauthed_client.post(self.url_change_password)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            f'{self.url_change_password} {response.status_code}'
            f'unauthed_client expected status = 401'
        )
        response = authed_user_client.post(self.url_change_password)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f'post {self.url_change_password} with empty data'
        )
        change_password_data = (
            ('pass@PASS1', 'asd@ASD123', 'asd@ASD123',
             status.HTTP_200_OK, 'valid data'),
            ('pass@PASS1', 'asd@ASD123', 'asd@A123SD',
             status.HTTP_400_BAD_REQUEST, 'different password'),
            ('pass@11234', 'asd@ASD123', 'asd@ASD123',
             status.HTTP_400_BAD_REQUEST, 'invalid current_password'),
            ('pass@PASS1', 'asd', 'asd',
             status.HTTP_400_BAD_REQUEST, 'password too simple'),
        )
        for (current_password, password, re_password,
             status_code, message) in change_password_data:
            data = {
                'current_password': current_password,
                'password': password,
                're_password': re_password,
            }
            response = authed_user_client.post(
                self.url_change_password, data=data
            )
            assert response.status_code == status_code, (message)

    def test_users_get_me(
        self,
        full_data_user_client,
        unauthed_client
    ):
        response = unauthed_client.get(self.url_me)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            f'{self.url_me} only for auth user'
        )
        response = full_data_user_client.get(self.url_me)
        assert response.status_code == status.HTTP_200_OK
        expected_data = {
            'email': 'fulldata@gmail.fake',
            'first_name': 'first',
            'last_name': 'last',
            'phone': '+79220011223',
            'birth_date': '2000-02-02',
            'occupation': 'string',
            'is_subscribed': False,
        }
        response_data = response.json()
        for key, value in expected_data.items():
            assert response_data[key] == value, (
                f'{key} {response_data[key]} not equal {value}'
            )

    def test_users_patch_me(
        self,
        authed_user_client,
        unauthed_client
    ):
        response = unauthed_client.patch(self.url_me)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            f'{self.url_me} only for auth user {response.status_code}'
        )
        data = {
            'first_name': 'new-first-name',
            'last_name': 'new-last-name',
            'phone': '+79223344556',
            'birth_date': '2002-02-02',
            'occupation': 'string'
        }
        request_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
        }
        response = authed_user_client.patch(self.url_me, data=request_data)
        assert response.status_code == status.HTTP_200_OK, (
            f'{self.url_me} change names status {response.status_code}'
        )
        assert response.json()['first_name'] == data['first_name'], (
            'updated first_name not equal'
        )
        assert response.json()['last_name'] == data['last_name'], (
            'updated last_name not equal'
        )
        phones_change_data = (
            (data['phone'], status.HTTP_200_OK),
            ('string', status.HTTP_400_BAD_REQUEST),
            ('+79221100111123', status.HTTP_400_BAD_REQUEST),
            ('79221100111', status.HTTP_400_BAD_REQUEST),
            ('3125151', status.HTTP_400_BAD_REQUEST),
        )
        for phone, status_code in phones_change_data:
            request_data = {'phone': phone}
            response = authed_user_client.patch(self.url_me, data=request_data)
            assert response.status_code == status_code, (
                f'patch{self.url_me} with {phone} {response.status_code}'
            )
        future_date = datetime.date.today() + datetime.timedelta(days=1)
        birth_day_change_data = (
            (data['birth_date'], status.HTTP_200_OK),
            (future_date, status.HTTP_400_BAD_REQUEST),
            ('2000-13-02', status.HTTP_400_BAD_REQUEST),
            ('2000-01-32', status.HTTP_400_BAD_REQUEST),
            ('2000.01.01', status.HTTP_400_BAD_REQUEST),
            ('2000', status.HTTP_400_BAD_REQUEST),
            ('01.2000.01', status.HTTP_400_BAD_REQUEST),
        )
        for birth_date, status_code in birth_day_change_data:
            request_data = {'birth_date': birth_date}
            response = authed_user_client.patch(self.url_me, data=request_data)
            assert response.status_code == status_code, (
                f'patch{self.url_me} with {birth_date} {response.status_code}'
            )
        request_data = {'occupation': 'string'}
        response = authed_user_client.patch(self.url_me, data=request_data)
        assert response.status_code == status.HTTP_200_OK
        response = authed_user_client.get(self.url_me)
        for key, value in data.items():
            assert response.json()[key] == value, (
                f'{self.url_me} {response.status_code}'
                f'{response.json()[key]} != {value}'
            )

    def test_reset_password(self, unauthed_client, full_data_user):
        data = {'email': full_data_user.email}
        response = unauthed_client.post(
            self.url_reset_password_code, data=data
        )
        assert response.status_code == status.HTTP_200_OK, (
            f'{self.url_reset_password_code} {response.status_code}'
            f'with exists user.email'
        )
        code = cache.get(full_data_user.id)
        valid_data = {
            'email': full_data_user.email,
            'confirmation_code': code,
            'password': 'string!!!',
            're_password': 'string!!!'
        }
        invalid_data_fields = (
            ('email', 'invalid@fake.com', status.HTTP_400_BAD_REQUEST),
            ('confirmation_code', '123321', status.HTTP_400_BAD_REQUEST),
            ('password', 'string!!!!', status.HTTP_400_BAD_REQUEST),
        )
        for field, value, status_code in invalid_data_fields:
            invalid_data = valid_data.copy()
            invalid_data[field] = value
            response = unauthed_client.post(
                self.url_reset_password, data=invalid_data
            )
            assert response.status_code == status_code, (
                f'{self.url_reset_password} {response.status_code}'
                f'{field}:{value} expected {status_code}'
            )
        response = unauthed_client.post(
            self.url_reset_password, data=valid_data
        )
        assert response.status_code == status.HTTP_200_OK, (
            f'{self.url_reset_password} {response.status_code} '
            f'with valid data {valid_data}'
        )
