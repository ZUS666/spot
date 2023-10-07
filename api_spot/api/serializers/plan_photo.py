from rest_framework import serializers

from spots.models import PlanPhoto


class PlanPhotoGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода фотографии плана.
    """

    class Meta:
        model = PlanPhoto
        fields = (
            'id',
            'location',
            'image',
        )
