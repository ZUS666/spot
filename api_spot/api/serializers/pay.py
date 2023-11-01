from django.core.validators import RegexValidator
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from api.serializers import PromocodeCheckSerializer
from api.services.promocode_check import promocode_available_check
from api.fields import GetOrderPay


class PaySerializer(serializers.Serializer):
    """Сериадизатор для оплаты."""
    order = serializers.HiddenField(
        default=GetOrderPay(),
    )
    name_owner = serializers.CharField(
        max_length=30, validators=(RegexValidator(r'^[A-Za-z]+$'),)
    )
    card_number = serializers.CharField(
        max_length=16, validators=(RegexValidator(r'^[\d]{16,16}$'),)
    )
    date = serializers.DateField(
        format='%m/%y',
        input_formats=('%m/%y', )
    )
    cvv = serializers.CharField(
        max_length=3, validators=(RegexValidator(r'^[\d]{1,3}$'),)
    )
    email = serializers.EmailField()
    phone = PhoneNumberField(region='RU')


class PaySimpleSerializer(PromocodeCheckSerializer):
    """Сериадизатор для оплаты с промокодом."""
    promocode = serializers.CharField(max_length=64, required=False,)

    def validate(self, data, *args, **kwargs):
        promocode_name = data.get('promocode')
        if not promocode_name:
            return data
        order = data.get('order')
        user = data.get('user')
        promocode = promocode_available_check(promocode_name, order.spot, user)
        data['promocode'] = promocode
        return data
