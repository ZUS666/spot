from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from api.fields import GetSpot
from spots.models.order import Order


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для брони."""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    spot = serializers.HiddenField(
        default=GetSpot()
    )
    spot_name = StringRelatedField(source='spot.name', read_only=True)

    class Meta:
        """Класс мета для модели Order."""
        model = Order
        fields = (
            'spot', 'user', 'spot_name',
            'date', 'start_time', 'end_time', 'bill'
        )

    def validate(self, data):
        """Проверка на пересечение с другими бронями."""
        spot = data.get('spot')
        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if end_time < start_time:
            raise serializers.ValidationError(
                {'start_date': 'Начало брони позже конца'})

        qs = Order.objects.filter(
            spot=spot,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        if qs.exists():
            raise serializers.ValidationError({
                'Spot': 'Данное время уже частиточно уже забранировано',
            })
        return data
