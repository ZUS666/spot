from django.core.validators import RegexValidator

from rest_framework import serializers


class PaySerializer(serializers.Serializer):
    name_owner = serializers.CharField(
        max_length=30, validators=(RegexValidator(r'^[A-Za-z]+$'),)
    )
    card_number = serializers.CharField(
        max_length=16, validators=(RegexValidator(r'^[\d]{16,16}$'),)
    )
    date = serializers.DateField(
        format='%m/%y',
        input_formats=['%m/%y', ]
    )
    cvv = serializers.CharField(
        max_length=3, validators=(RegexValidator(r'^[\d]$'),)
    )
    email = serializers.EmailField()
    phone = serializers.IntegerField()
