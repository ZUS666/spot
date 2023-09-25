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
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = (
            'name',
            'street',
            'house_number',
            'open_time',
            'close_time',
            'latitude',
            'longitude',
            'plan_photo',
            'extra_photo',
            'description',
            'is_favorited',
            # 'count_workspace',
            # 'count_meeting_room',
        )

    def get_is_favorited(self, instance, *args, **kwargs):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return instance.favorites.filter(user_id=user.id).exists()
