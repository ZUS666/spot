from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from api.fields import GetLocation
from spots.models.favorite import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного."""
    location = serializers.HiddenField(
        default=GetLocation()
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    location_name = StringRelatedField(
        source='location.name', read_only=True
    )

    class Meta:
        model = Favorite
        fields = ('id', 'location', 'user', 'location_name',)
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('location', 'user'),
                message='Уже есть в избранном'
            ),
        )
