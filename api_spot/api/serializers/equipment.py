from rest_framework import serializers

from api.fields import GetLocation
from spots.models import SpotEquipment


class EquipmentGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода cнаряжений.
    """
    location = serializers.HiddenField(
        default=GetLocation()
    )
    name = serializers.CharField(source='equipment.name')
    icon = serializers.CharField(source='equipment.icon')
    category = serializers.CharField(source='spot.category')

    class Meta:
        model = SpotEquipment
        fields = ('id', 'name', 'icon', 'location', 'category',)
