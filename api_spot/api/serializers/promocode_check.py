from rest_framework import serializers

from api.services.promocode_check import promocode_available_check


class PromocodeCheckSerializer(serializers.Serializer):
    promocode = serializers.CharField(max_length=64)

    def validate_promocode(self, value, *args, **kwargs):
        promocode_available_check(value)
