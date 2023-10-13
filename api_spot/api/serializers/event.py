from rest_framework import serializers

from information.models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода мероприятий.
    """

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'image',
            'address',
            'meeting_quantity',
            'url',
            'date',
        )
