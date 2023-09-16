from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from spots.models.review import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""
    first_name = StringRelatedField(source="user.first_name", read_only=True)
    last_name = StringRelatedField(source="user.last_name", read_only=True)

    class Meta:
        """Класс мета для модели Review."""
        model = Review
        fields = (
            "description", "raiting", "first_name", "last_name", "pub_date"
        )
