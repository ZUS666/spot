from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from spots.models.order import Order


class ReservationSerializer(serializers.ModelSerializer):
    """Сериализатор для брони."""
    spot = StringRelatedField(source='spot.name', read_only=True)
    name = StringRelatedField(source='user.first_name', read_only=True)
    surname = StringRelatedField(source='user.last_name', read_only=True)
    duration = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Класс мета для модели Review."""
        model = Order
        fields = (
            "spot", "name", "surname",
            "start_date", "end_date", "duration"
        )

    def get_duration(self, obj):
        time = obj.end_date - obj.start_date
        return f"{time.total_seconds()} в секундах"
