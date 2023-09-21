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

    def create(self, validated_data):
        spot = validated_data.pop('spot')
        spot = get_object_or_404(
            Spot,
            number=spot.get('number'),
            category__name=spot.get('category').get('name')
        )
        validated_data['spot'] = spot
        order = Order.objects.create(**validated_data)
        return order

    def validate(self, data):
        """Проверка на пересечение с другими бронями."""
        spot = data.get('spot')
        spot = get_object_or_404(
            Spot,
            number=spot.get('number'),
            category__name=spot.get('category').get('name')
        )
        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if end_time <= start_time:
            raise serializers.ValidationError(
                {'start_date': 'Начало брони позже конца'})

        qs = Order.objects.filter(
            spot=spot,
            date=date,
            start_time__lte=end_time,
            end_time__gte=start_time
        )
        if qs.exists():
            raise serializers.ValidationError({
                'Spot': 'Данное время уже частиточно уже забранировано',
            })
        return data
