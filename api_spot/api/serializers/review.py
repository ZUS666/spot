from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from spots.models.review import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""
    name = StringRelatedField(source="user.first_name", read_only=True)
    surname = StringRelatedField(source="user.last_name", read_only=True)

    class Meta:
        """Класс мета для модели Review."""
        model = Review
        fields = (
            "description", "raiting", "name", "surname", "pub_date"
        )
