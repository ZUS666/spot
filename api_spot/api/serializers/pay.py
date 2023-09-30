from django.core.validators import RegexValidator
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from api.fields import GetOrderPay
from api.serializers.order import OrderUpdateSerializer


class PaySerializer(serializers.Serializer):
    """Сериадизатор для оплаты."""
    order = OrderUpdateSerializer(
        default=GetOrderPay(),
        read_only=True
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
