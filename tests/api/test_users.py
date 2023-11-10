import pytest
from django.core.cache import cache
from rest_framework import status


@pytest.mark.django_db(transaction=True)
class TestUserRegistration:
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
                'status 400 for invalid data'
            )

    def test_valid_data_signup(self, unauthed_client, django_user_model):
        """
        Тестирование регистрации пользователя.
        """
        assert django_user_model.objects.count() == 0
        response = unauthed_client.post(self.url_signup, data=self.data)
        assert response.status_code == status.HTTP_201_CREATED, (
            'status 201 registration user'
        )
        assert django_user_model.objects.count() == 1
        first_user = django_user_model.objects.get(id=1)
        assert first_user.is_active is False
        response = unauthed_client.post(self.url_signup, data=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            'status 400 user exists'
        )
        data_resend = {
            'email': self.data['email']
        }
        response = unauthed_client.post(
            self.url_resend_confirmation_code,
            data=data_resend,
        )
        assert response.status_code == status.HTTP_200_OK, (
            'status 200 on resend code'
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
                f'activation with data {email} {confirmation_code}'
                f'{status_code}'
            )
        first_user.refresh_from_db()
        assert first_user.is_active is True


@pytest.mark.django_db(transaction=True)
class TestUserActions:
    url_change_password = '/api/v1/users/change_password/'
    url_me = '/api/v1/users/me/'

    def test_user_change_password(
        self,
        authed_user_client,
        unauthed_client,
    ):
        response = unauthed_client.post(self.url_change_password)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            f'{self.url_change_password} only for authed user'
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
        full_data_user,
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
