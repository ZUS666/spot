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
    spot_name = StringRelatedField(source="spot.name", read_only=True)
    first_name = StringRelatedField(source="user.first_name", read_only=True)
    last_name = StringRelatedField(source="user.last_name", read_only=True)
    duration = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Класс мета для модели Review."""
        model = Order
        fields = (
            "spot", "user", "spot_name", "first_name", "last_name",
            "start_date", "end_date", "duration"
        )

    def get_duration(self, obj):
        """Получение продолжительность брони."""
        time = obj.end_date - obj.start_date
        return f"{round((time.total_seconds() / 3600), 3)} в часах"

    def validate(self, data):
        """Проверка на пересечение с другими бронями."""
        spot = data.get("spot")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if end_date < start_date:
            raise serializers.ValidationError(
                {"start_date": "Начало брони позже конца"})

        qs = Order.objects.filter(
            spot=spot,
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        if qs.exists():
            raise serializers.ValidationError({
                "Spot": ("Данный коворкинг уже забронирован", ),
            })
        return data
