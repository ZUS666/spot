from rest_framework import serializers

from spots.models import Category


class CategoriesGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода категорий.
    """

    class Meta:
        model = Category
        fields = '__all__'
