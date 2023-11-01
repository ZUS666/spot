from rest_framework import serializers

from api.services.promocode_check import promocode_available_check
from api.fields import GetSpot


class PromocodeCheckSerializer(serializers.Serializer):
    promocode = serializers.CharField(max_length=64)
    spot = serializers.HiddenField(
        default=GetSpot()
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data, *args, **kwargs):
        promocode_name = data.get('promocode')
        spot = data.get('spot')
        user = data.get('user')
        promocode = promocode_available_check(promocode_name, spot, user)
        data['promocode'] = promocode
        return data
