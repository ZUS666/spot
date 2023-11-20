from rest_framework import serializers

from users.models import Avatar


class UserAvatarInputSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    image = serializers.ImageField()


class UserAvatarOutputSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Avatar
        fields = ('image',)
