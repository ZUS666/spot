from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from api.fields import GetOrder
from spots.models.review import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    booked_spot = serializers.HiddenField(default=GetOrder())
    first_name = StringRelatedField(source='user.first_name', read_only=True)
    last_name = StringRelatedField(source='user.last_name', read_only=True)

    class Meta:
        """Класс мета для модели Review."""
        model = Review
        fields = (
            'booked_spot',
            'description', 'rating', 'user',
            'first_name', 'last_name', 'pub_date'
        )

    def validate(self, data):
        """Валидация данных из модели."""
        self.Meta.model(**data).full_clean()
        return super().validate(data)


class ReviewGetSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов для получения."""
    first_name = StringRelatedField(source='user.first_name', read_only=True)
    last_name = StringRelatedField(source='user.last_name', read_only=True)

    class Meta:
        """Класс мета для модели Review."""
        model = Review
        fields = (
            'description', 'rating',
            'first_name', 'last_name', 'pub_date'
        )
