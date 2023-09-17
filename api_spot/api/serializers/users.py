from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации и получения подробной информации
    о пользователе.
    """
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    default_error_messages = {
        'password_mismatch': 'Пароли не совпадают'
    }

    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'first_name',
            'telegram',
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
        attrs = super().validate(attrs)
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
            'first_name',
            'last_name',
            'phone',
            'telegram'
        )


class ActivationUserSerializer(serializers.Serializer):
    """
    Сериализатор для активации пользователя через
    ввод кода подтверждения с эл. почты.
    """
    email = serializers.EmailField()
    confirmation_code = serializers.IntegerField()


class SendConfirmationCodeSerializer(serializers.Serializer):
    """
    Сериализатор для отправки кода подтверждения.
    """
    email = serializers.EmailField()
