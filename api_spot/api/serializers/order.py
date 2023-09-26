import datetime
from decimal import Decimal

from django.conf import settings
from rest_framework import serializers

from spots.models.order import Order
from api.serializers.spot import SpotSerializer
from api.fields import GetSpot


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для брони."""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    spot = SpotSerializer(
        default=GetSpot()
    )
    price = serializers.SerializerMethodField()
    price_time = serializers.SerializerMethodField()
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
            'price', 'price_time'
        )

    def get_price(self, obj):
        """Цена по старте и конце."""
        end = datetime.datetime.strptime(
            f'{obj.date} {obj.end_time}', '%Y-%m-%d %H:%M:%S'
        )
        start = datetime.datetime.strptime(
            f'{obj.date} {obj.start_time}', '%Y-%m-%d %H:%M:%S'
        )
        timedelta = Decimal((end - start).total_seconds() / 3600)
        return obj.spot.price.total_price * timedelta

    # def get_price_time(self, obj):
    #     """Цена по time."""
    #     return obj.spot.price.total_price * len(obj.time)

    def validate(self, data):
        """Проверка на пересечение с другими бронями."""
        self.Meta.model(**data).full_clean()
        return super().validate(data)
