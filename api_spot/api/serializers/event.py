from rest_framework import serializers

from spots.models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода мероприятий.
    """

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'address',
            'meeting_quantity',
            'url',
            'date',
        )
