from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from spots.models.order import Order


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для брони."""
    spot = StringRelatedField(source="spot.name", read_only=True)
    name = StringRelatedField(source="user.first_name", read_only=True)
    surname = StringRelatedField(source="user.last_name", read_only=True)
    duration = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Класс мета для модели Review."""
        model = Order
        fields = (
            "spot", "name", "surname",
            "start_date", "end_date", "duration"
        )

    def get_duration(self, obj):
        """Получение продолжительность брони."""
        time = obj.end_date - obj.start_date
        return f"{round((time.total_seconds() / 3600), 3)} в часах"

    def validate(self, data):
        """Проверка на пересечение с другими бронями."""
        spot_id = self.context.get("spot_id")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if end_date < start_date:
            raise serializers.ValidationError(
                {"start_date": "Начало брони позже конца"})

        qs = Order.objects.filter(
            spot=spot_id,
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        if qs.exists():
            raise serializers.ValidationError({
                "Spot": ("Данный коворкинг уже забронирован", ),
            })
        return data
