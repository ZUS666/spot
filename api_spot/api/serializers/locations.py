from rest_framework import serializers

# from spots.constants import MEETING_ROOM, WORK_SPACE
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
    # count_workspace = serializers.SerializerMethodField()
    # count_meeting_room = serializers.SerializerMethodField()
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

    # def get_count_workspace(self, instance, *args, **kwargs):
    #     return instance.spots.filter(category=WORK_SPACE).count()

    # def get_count_meeting_room(self, instance, *args, **kwargs):
    #     return instance.spots.filter(category=MEETING_ROOM).count()
