from rest_framework import serializers

from spots.models import Spot, Order


class SpotSerializer(serializers.ModelSerializer):
    """Сериализатор модели спота."""
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
    is_ordered = serializers.SerializerMethodField(default=False)

    class Meta:
        """Класс мета для модели Spot."""
        model = Spot
        fields = (
            'name',
            'description',
            'price',
            'location',
            'category',
            'equipment',
            'is_ordered',
        )

    def get_is_ordered(self, instance, *args, **kwargs):
        query_params = self.context.get('request').query_params
        # if 'date' and 'start_time' and 'end_time' in query_params.keys():
        #     date = query_params.get('date')
        #     start_time = query_params.get('start_time')
        #     end_time = query_params.get('end_time')
        #     return Order.objects.filter(
        #         date=date,
        #         start_time=start_time,
        #         end_time=end_time
        #     ).exists()
        return False