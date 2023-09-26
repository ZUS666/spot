from django.conf import settings
from rest_framework import serializers

from spots.models import Location
from .extra_photo import ExtraPhotoGetSerializer


class LocationGetPlanNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'name',
            'plan_photo',
        )


class LocationGetShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = (
            'name',
            'city',
            'street',
            'house_number',
            'metro',
            'rating',
            'low_price',
            'main_photo',
        )


class LocationGetSerializer(serializers.ModelSerializer):
    open_time = serializers.TimeField(format=settings.TIME_FORMAT)
    close_time = serializers.TimeField(format=settings.TIME_FORMAT)
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
            'city',
            'street',
            'house_number',
            'metro',
            'open_time',
            'close_time',
            'rating',
            'low_price',
            'main_photo',
            'extra_photo',
            'rating',
            'low_price',
            'description',
            'is_favorited',
        )

    def get_is_favorited(self, instance, *args, **kwargs):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return instance.favorites.filter(user_id=user.id).exists()
