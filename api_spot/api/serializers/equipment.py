from api.fields import GetLocation
from rest_framework import serializers
from spots.models import SpotEquipment


class EquipmentGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода cнаряжений.
    """
    location = serializers.HiddenField(
        default=GetLocation()
    )
    name = serializers.CharField(source='equipment.name')
    category = serializers.CharField(source='spot.category')

    class Meta:
        model = SpotEquipment
        fields = ('name', 'location', 'category')
