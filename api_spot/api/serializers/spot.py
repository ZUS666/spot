from rest_framework import serializers

from spots.models import Spot


class SpotSerializer(serializers.ModelSerializer):
    """Сериализатор модели спота."""
    category_name = serializers.CharField(source='category.name')

    class Meta:
        """Класс мета для модели Spot."""
        model = Spot
        fields = (
            'number', 'category_name'
        )
