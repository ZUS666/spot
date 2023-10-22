from decimal import Decimal

from django.conf import settings
from rest_framework import serializers

from spots.models import Location

from .extra_photo import ExtraPhotoGetSerializer


class LocationGetSerializer(serializers.Serializer):
    """
    Сериализатор для вывода подбробной информации о локации.
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    get_full_address_str = serializers.CharField()
    metro = serializers.CharField()
    open_time = serializers.TimeField(format=settings.TIME_FORMAT)
    close_time = serializers.TimeField(format=settings.TIME_FORMAT)
    minprice = serializers.DecimalField(max_digits=10, decimal_places=2)
    main_photo = serializers.ImageField()
    extra_photo = ExtraPhotoGetSerializer(
        many=True,
        read_only=True,
        source='location_extra_photo'
    )
    rating_1 = serializers.DecimalField(max_digits=3, decimal_places=2)
    short_annotation = serializers.CharField()
    description = serializers.CharField()
    is_favorited = serializers.BooleanField()
    workspace = serializers.IntegerField()
    meetings = serializers.IntegerField()
    coordinates = serializers.SerializerMethodField()
    days_open = serializers.CharField()

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
