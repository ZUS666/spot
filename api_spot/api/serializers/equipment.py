from rest_framework import serializers

from spots.models import SpotEquipment


class EquipmentGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода оборудование.
    """
    name = serializers.CharField(source='equipment.name')
    icon = serializers.FileField(source='equipment.icon')
    category = serializers.CharField(source='spot.category')

    class Meta:
        model = SpotEquipment
        fields = ('id', 'name', 'icon', 'category',)
