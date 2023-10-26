
from rest_framework import serializers

from api.fields import Base64ImageField
from users.models import Avatar


class AvatarSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Avatar
        fields = ('id', 'image',)
