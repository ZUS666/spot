from decimal import Decimal

from django.conf import settings
from rest_framework import serializers

from spots.models import Location

from .extra_photo import ExtraPhotoGetSerializer


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
    low_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    is_favorited = serializers.BooleanField()
    count_workspace = serializers.IntegerField()
    count_meeting_room = serializers.IntegerField()
    coordinates = serializers.SerializerMethodField()


    class Meta:
        model = Location
        fields = (
            'id',
            'name',
            'get_full_address_str',
            'metro',
            'open_time',
            'close_time',
            'low_price',
            'main_photo',
            'extra_photo',
            'rating',
            'short_annotation',
            'description',
            'is_favorited',
            'count_workspace',
            'count_meeting_room',
            'coordinates',
            'days_open'
        )

    def get_coordinates(self, instance) -> list[Decimal]:
        """
        Список координат
        """
        return [instance.latitude, instance.longitude, ]


class LocationGetShortSerializer(LocationGetSerializer):
    """
    Сериализатор для вывода краткой информации о локации.
    Используется на главной странице.
    """

    class Meta:
        model = Location
        fields = (
            'id',
            'name',
            'get_full_address_str',
            'metro',
            'rating',
            'low_price',
            'main_photo',
            'is_favorited',
        )


class LocationMapSerializer(LocationGetSerializer):
    """
    Сериализатор для отображения на карте.
    """
    small_photo = serializers.ImageField(source='small_main_photo.image')

    class Meta:
        model = Location
        fields = (
            'id',
            'name',
            'get_full_address_str',
            'metro',
            'rating',
            'small_photo',
            'coordinates',
        )
