from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from spots.models.favorite import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного."""
    id = serializers.IntegerField(source="location.id", read_only=True)
    name = StringRelatedField(source="location.street", read_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "name", "pub_date")

    def validate(self, data):
        """Проверка на повтор."""
        location_id = self.context.get("location_id")
        user_id = self.context.get("request").user.id
        if Favorite.objects.filter(
            user=user_id, location=location_id
        ).exists():
            raise serializers.ValidationError({
                "location": "Данный location уже в избранном"
            })
        return data
