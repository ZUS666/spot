from django.conf import settings
from rest_framework import serializers

from api.fields import GetSpot
from api.serializers.spot import SpotDetailSerializer
from spots.models.order import Order


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для брони."""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    spot = SpotDetailSerializer(
        default=GetSpot()
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
            'user', 'spot', 'date',
            'start_time', 'end_time',
            'bill',
        )

    def validate(self, data):
        """Проверка на пересечение с другими бронями."""
        self.Meta.model(**data).full_clean()
        return super().validate(data)
