import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from users.models import Avatar


class Base64ImageField(serializers.ImageField):
    """Класс раскодировки изображения."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class AvatarSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Avatar
        fields = ('id', 'image',)
