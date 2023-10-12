from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.exceptions import (
    ConfirmationCodeInvalidError, EmailNotFoundError, UserIsActiveError,
)
from api.mixins import CreateDestroyViewSet
from api.permissions import UserDeletePermission
from api.serializers.users import (
    ChangePasswordSerializer, ConfirmationCodeSerializer,
    ResetPasswordSerializer, SendCodeSerializer, UserMeSerializer,
    UserSerializer,
)
from api.services.users import (
    cache_and_send_confirmation_code, finish_activation_email,
    finish_reset_password_email, registration_email, reset_password_email,
)


User = get_user_model()


class UserViewSet(CreateDestroyViewSet):
    """
    post: Представление для регистрации пользователей с отправкой кода
    подтверждения.
    delete: Представления для удаления своего аккаунта пользователем.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserDeletePermission,)

    def get_permissions(self):
        """
        Предоставление прав на создание для неавторизованного пользователя.
        """
        if self.action == 'create':
            return (AllowAny(),)
        return super().get_permissions()

    def perform_create(self, serializer, *args, **kwargs):
        """
        Создание и отправка пароля после успешной регистрации пользователя.
        """
        user = serializer.save(*args, **kwargs)
        cache_and_send_confirmation_code(user, registration_email)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(AllowAny,),
        serializer_class=ConfirmationCodeSerializer
    )
    def activation(self, request, *args, **kwargs):
        """
        Активация юзера через код подтверждения.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = User.objects.filter(email=email).first()
        if not user:
            raise EmailNotFoundError
        if confirmation_code != cache.get(user.id):
            raise ConfirmationCodeInvalidError
        user.is_active = True
        user.save()
        finish_activation_email(user)
        return Response(
            {'message': 'Электронная почта верифицирована'},
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(IsAuthenticated,),
        serializer_class=ChangePasswordSerializer
    )
    def change_password(self, request, *args, **kwargs):
        """
        Cмена пароля авторизованного пользователя.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        user = serializer.validated_data.get('user')
        user.set_password(password)
        user.save(update_fields=['password'])
        return Response(
            {'message': 'Пароль изменен'}, status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(AllowAny,),
        serializer_class=ResetPasswordSerializer
    )
    def reset_password(self, request, *args, **kwargs):
        """
        Сброс пароля с последующим удаленим токена авторизации.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        password = serializer.validated_data.get('password')
        user = User.objects.filter(email=email).first()
        if not user:
            raise EmailNotFoundError
        if confirmation_code != cache.get(user.id):
            raise ConfirmationCodeInvalidError
        user.set_password(password)
        user.save(update_fields=['password'])
        user.auth_token.delete()
        finish_reset_password_email(user)
        return Response(
            {'message': 'Пароль изменен'},
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=UserMeSerializer
    )
    def me(self, request, *args, **kwargs):
        """
        Получение пользователем информации информацию о себе.
        """
        email = request.user.email
        user = User.objects.get(email=email)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @me.mapping.patch
    def patch_me(self, request, *args, **kwargs):
        """
        Изменение пользователем информации о себе.
        """
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(AllowAny,),
        serializer_class=SendCodeSerializer
    )
    def reset_password_confirmation_code(self, request, *args, **kwargs):
        """
        Отправка кода подтверждения для сброса пароля.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            raise EmailNotFoundError
        cache_and_send_confirmation_code(user, reset_password_email)
        return Response(
            {'message': 'Код подтверждения отправлен на почту'},
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(AllowAny,),
        serializer_class=SendCodeSerializer
    )
    def resend_confirmation_code(self, request, *args, **kwargs):
        """
        Повторная отправка кода подтверждения.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            raise EmailNotFoundError
        if user.is_active:
            raise UserIsActiveError
        cache_and_send_confirmation_code(user, registration_email)
        return Response(
            {'message': 'Код активации отправлен на почту'},
            status=status.HTTP_200_OK
        )
