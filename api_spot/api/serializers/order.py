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
    price = serializers.DecimalField(
        source='spot.price',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        """Класс мета для модели Order."""
        model = Order
        fields = (
            'user', 'spot', 'date',
            'start_time', 'end_time', 'price'
        )

    def validate(self, data):
        """Проверка на пересечение с другими бронями."""
        self.Meta.model(**data).full_clean()
        return super().validate(data)
