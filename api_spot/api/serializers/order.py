from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from api.fields import GetSpot
from spots.models.order import Order
from spots.constants import TIME_CHOICES


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для брони."""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    spot = serializers.HiddenField(
        default=GetSpot()
    )
    spot_name = StringRelatedField(source='spot.name', read_only=True)
    time = serializers.MultipleChoiceField(choices=TIME_CHOICES)

    class Meta:
        """Класс мета для модели Order."""
        model = Order
        fields = (
            'spot', 'user', 'spot_name',
            'date', 'time', 'bill'
        )

    # def validate(self, data):
    #     """Проверка на пересечение с другими бронями."""
    #     spot = data.get('spot')
    #     start_date = data.get('start_date')
    #     end_date = data.get('end_date')

    #     if end_date < start_date:
    #         raise serializers.ValidationError(
    #             {'start_date': 'Начало брони позже конца'})

    #     qs = Order.objects.filter(
    #         spot=spot,
    #         start_date__lt=end_date,
    #         end_date__gt=start_date
    #     )
    #     if qs.exists():
    #         raise serializers.ValidationError({
    #             'Spot': 'Данный коворкинг уже забронирован',
    #         })
    #     return data
