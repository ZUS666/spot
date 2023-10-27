from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from api.fields import LowercaseEmailField


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации и получения подробной информации
    о пользователе.
    """
    password = serializers.CharField(write_only=True, max_length=128)
    re_password = serializers.CharField(write_only=True, max_length=128)
    default_error_messages = {
        'password_mismatch': 'Пароли не совпадают'
    }

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            're_password',
        )

    def validate(self, attrs):
        """
        Добавлена валидация пароля на совпадение и корректность в
        соответсвии с настройками валидции пароля (AUTH_PASSWORD_VALIDATORS).
        """
        self.fields.pop('re_password')
        re_password = attrs.pop('re_password')
        password = attrs['password']
        if re_password == password:
            user = User(**attrs)
            validate_password(password, user)
            return attrs
        return self.fail('password_mismatch')

    def create(self, validated_data):
        """
        Вызывает создание обычного юзера.
        """
        return User.objects.create_user(**validated_data)


class UserMeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения пользователем данных о себе
    и их изменения.
    """
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'birth_date',
            'occupation',
            'is_subscribed'
        )
        read_only_fields = ('email', 'is_subscribed')


class EmailSerializer(serializers.Serializer):
    """
    Сериализатор c полем email.
    """
    email = LowercaseEmailField()


class SendCodeSerializer(EmailSerializer):
    """
    Сериализатор для отправки кода подтверждения.
    """
    pass


class ConfirmationCodeSerializer(EmailSerializer):
    """
    Сериализатор для активации пользователя через
    ввод кода подтверждения с эл. почты.
    """
    confirmation_code = serializers.IntegerField()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Сериализатор для смены пароля юзера.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    current_password = serializers.CharField(write_only=True, max_length=128)
    password = serializers.CharField(write_only=True, max_length=128)
    re_password = serializers.CharField(write_only=True, max_length=128)
    default_error_messages = {
        'password_mismatch': 'Новый пароль не совпадает с повторным вводом',
        'invalid_password': 'Текущий пароль не верный'
    }

    def validate_current_password(self, value):
        """
        Валидация текущего пароля.
        """
        is_password_valid = self.context['request'].user.check_password(value)
        if is_password_valid:
            return value
        else:
            self.fail("invalid_password")

    def validate(self, attrs):
        """
        Валидация пароля на совпадение и корректность в
        соответсвии с настройками валидции пароля (AUTH_PASSWORD_VALIDATORS).
        """
        re_password = attrs.pop('re_password')
        password = attrs['password']
        user = self.context['request'].user
        if re_password == password:
            validate_password(password, user)
            return attrs
        return self.fail('password_mismatch')


class ResetPasswordSerializer(serializers.Serializer):
    """
    Сериализатор для установки нового пароля после сброса.
    """
    email = LowercaseEmailField()
    confirmation_code = serializers.IntegerField()
    password = serializers.CharField(write_only=True, max_length=128)
    re_password = serializers.CharField(write_only=True, max_length=128)
    default_error_messages = {
        'password_mismatch': 'Новый пароль не совпадает с повторным вводом',
    }

    def validate(self, attrs):
        """
        Валидация пароля на совпадение и корректность в
        соответсвии с настройками валидции пароля (AUTH_PASSWORD_VALIDATORS).
        """
        re_password = attrs.pop('re_password')
        password = attrs['password']
        if re_password == password:
            validate_password(password, User(email=attrs['email']))
            return attrs
        return self.fail('password_mismatch')
