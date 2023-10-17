from django.conf import settings
from rest_framework import serializers

from api.fields import GetSpot
from spots.models.order import Order


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для брони."""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    spot = serializers.HiddenField(
        default=GetSpot(),
    )
    start_time = serializers.TimeField(
        format=settings.TIME_FORMAT
    )
    end_time = serializers.TimeField(
        format=settings.TIME_FORMAT
    )

    class Meta:
        """Класс мета для модели Order."""
        model = Order
        fields = (
            'id', 'user', 'spot',
            'date', 'start_time',
            'end_time', 'bill',
        )
        read_only_fields = ('bill',)

    def validate(self, data):
        """Проверка на пересечение с другими бронями."""
        self.Meta.model(**data).full_clean()
        return super().validate(data)


class OrderGetSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(
        format=settings.TIME_FORMAT
    )
    end_time = serializers.TimeField(
        format=settings.TIME_FORMAT
    )
    location_id = serializers.IntegerField(source='spot.location.id')
    location_name = serializers.StringRelatedField(source='spot.location.name')
    location_photo = serializers.ImageField(source='spot.location.main_photo')

    class Meta:
        """Класс мета для модели Order."""
        model = Order

        fields = (
            'id', 'date',
            'start_time', 'end_time', 'status',
            'location_id', 'spot',
            'location_name', 'location_photo',
            'bill'
        )


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения брони."""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    spot = serializers.HiddenField(
        default=GetSpot()
    )
    status = serializers.CharField(read_only=True)

    class Meta:
        """Класс мета для модели Order."""
        model = Order
        fields = (
            'id', 'user', 'spot', 'status',
        )
