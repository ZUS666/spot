from rest_framework import serializers

from users.models import Avatar


class UserAvatarInputSerializer(serializers.Serializer):
    """
    Сериализатор добавления/изменения аватара пользователя.
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    image = serializers.ImageField()


class UserAvatarOutputSerializer(serializers.ModelSerializer):
    """
    Сериализатор вывода аватара при сохранении.
    """
    image = serializers.ImageField()

    class Meta:
        model = Avatar
        fields = ('image',)
