from rest_framework import serializers

from api.validators import ListNamesValidator
from spots.constants import CATEGORY_CHOICES
from spots.models import Equipment, Price


class AddSpotsSerializer(serializers.Serializer):
    names = serializers.CharField(
        validators=(ListNamesValidator(),))
    price_id = serializers.SlugRelatedField(
        queryset=Price.objects.all(),
        slug_field='id'
    )
    category = serializers.ChoiceField(choices=CATEGORY_CHOICES)
    description = serializers.CharField(max_length=500)
    equipments_id = serializers.SlugRelatedField(
        queryset=Equipment.objects.all(),
        many=True,
        slug_field='id',
    )
