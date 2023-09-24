from rest_framework import serializers

from spots.models import Location
from .extra_photo import ExtraPhotoGetSerializer


class LocationsGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода локаций.
    """
    extra_photo = ExtraPhotoGetSerializer(
        many=True,
        read_only=True,
        source='location_extra_photo'
    )

    class Meta:
        model = Location
        fields = (
            'name',
            'street',
            'house_number',
            'latitude',
            'longitude',
            'plan_photo',
            'extra_photo',
            'description',
        )
