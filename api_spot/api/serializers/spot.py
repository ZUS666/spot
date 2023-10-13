from django.conf import settings
from rest_framework import serializers

from api.services.orders import is_ordered_spot
from spots.models import Spot


class SpotQuerySerializer(serializers.Serializer):
    """
    Сериализатор для валидации query_params.
    """
    date = serializers.DateField(input_formats=(settings.DATE_FORMAT,))
    start_time = serializers.TimeField(
        input_formats=(settings.TIME_FORMAT,)
    )
    end_time = serializers.TimeField(
        input_formats=(settings.TIME_FORMAT,)
    )

    class Meta:
        fields = ('date', 'start_time', 'end_time',)


class SpotSerializer(serializers.ModelSerializer):
    """Сериализатор получения объектов спота."""
    price = serializers.SlugRelatedField(
        read_only=True,
        slug_field='total_price'
    )
    is_ordered = serializers.SerializerMethodField(default=False)

    class Meta:
        """Класс мета для модели Spot."""
        model = Spot
        fields = (
            'id',
            'name',
            'price',
            'category',
            'is_ordered',
        )

    def get_is_ordered(self, instance, *args, **kwargs) -> bool:
        """
        Получение булевого значение по параметрам запроса о
        возможности бронирования.
        """
        date = self.context.get('date')
        start_time = self.context.get('start_time')
        end_time = self.context.get('end_time')
        return is_ordered_spot(instance, date, start_time, end_time)


class SpotDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для получения детальной информации о споте."""
    price = serializers.SlugRelatedField(
        read_only=True,
        slug_field='total_price'
    )
    location = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    equipment = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )

    class Meta:
        """Класс мета для модели Spot."""
        model = Spot
        fields = (
            'id',
            'name',
            'description',
            'price',
            'location',
            'category',
            'equipment',
        )
