from rest_framework import serializers

from spots.models import ExtraPhoto


class ExtraPhotoGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода дополнительных фото.
    """

    class Meta:
        model = ExtraPhoto
        fields = (
            'id',
            'image',
        )
