from django.conf import settings
from rest_framework import serializers

from spots.models import Location

from .extra_photo import ExtraPhotoGetSerializer


class LocationGetPlanNameSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода краткой информации о локации.
    Используется при выборе места бронирования.
    """
    class Meta:
        model = Location
        fields = (
            'id',
            'name',
            'plan_photo',
        )


class LocationGetShortSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода краткой информации о локации.
    Используется на главной странице.
    """

    class Meta:
        model = Location
        fields = (
            'id',
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
    """
    Сериализатор для вывода подбробной информации о локации.
    """
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
            'id',
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
        """
        Отображение наличия location в избранном при листинге location.
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return instance.favorites.filter(user_id=user.id).exists()
