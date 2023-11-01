from rest_framework import serializers

from api.services.promocode_check import promocode_available_check
from api.fields import GetOrder


class PromocodeCheckSerializer(serializers.Serializer):
    promocode = serializers.CharField(max_length=64)
    order = serializers.HiddenField(
        default=GetOrder()
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data, *args, **kwargs):
        promocode_name = data.get('promocode')
        order = data.get('order')
        user = data.get('user')
        promocode = promocode_available_check(promocode_name, order.spot, user)
        data['promocode'] = promocode
        return data
