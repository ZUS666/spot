from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from spots.models.favorite import Favorite
from api.fields import GetLocation


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного."""
    location = serializers.HiddenField(
        default=GetLocation()
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    street = StringRelatedField(
        source="location.street", read_only=True
    )

    class Meta:
        model = Favorite
        fields = ("location", "user", "street", "pub_date", )
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('location', 'user'),
                message="Уже есть в избранном"
            ),
        )
