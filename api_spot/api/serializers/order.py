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

    class Meta:
        """Класс мета для модели Order."""
        model = Order
        fields = (
            'user', 'spot',
            'date', 'start_time', 'end_time', 'bill'
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
