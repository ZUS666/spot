from django.shortcuts import get_object_or_404
from rest_framework import serializers

from spots.models.order import Order, Spot
from api.serializers.spot import SpotSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для брони."""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    spot = SpotSerializer()
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
        spot = data.get('spot')
        spot_obj = get_object_or_404(
            Spot,
            name=spot.get('name'),
            category__name=spot.get('category').get('name')
        )
        data['spot'] = spot_obj
        self.Meta.model(**data).full_clean()
        return super().validate(data)
