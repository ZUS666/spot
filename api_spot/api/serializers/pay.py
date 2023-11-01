from django.core.validators import RegexValidator
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from api.serializers import PromocodeCheckSerializer
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
    promo = PromocodeCheckSerializer(required=False)


class PaySimpleSerializer(serializers.Serializer):
    """Сериадизатор для оплаты."""
    promo = PromocodeCheckSerializer(required=False,)
