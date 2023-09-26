import base64

from django.core.files.base import ContentFile
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from spots.models import Location, Order, Spot


class GetLocation(serializers.CurrentUserDefault):
    """Получение локации из view."""
    def __call__(self, serializer_field):
        return get_object_or_404(
            Location,
            id=int(
                serializer_field.context.get('view').kwargs.get('location_id')
            )
        )


class GetSpot(serializers.CurrentUserDefault):
    """Получение spot из view."""
    def __call__(self, serializer_field):
        location = get_object_or_404(
            Location,
            id=int(
                serializer_field.context.get('view').kwargs.get('location_id')
            )
        )
        print(location)
        spots = Spot.objects.filter(location=location)
        print(spots)
        number = int(serializer_field.context.get('view').kwargs.get('spot_id')) - 1
        try:
            return spots[number]
        except IndexError:
            raise Http404


class GetOrder(serializers.CurrentUserDefault):
    """Получение order из view."""
    def __call__(self, serializer_field):
        return get_object_or_404(
            Order,
            id=int(
                serializer_field.context.get('view').kwargs.get('order_id')
            )
        )


class LowercaseEmailField(serializers.EmailField):
    """
    Приводит email к нижнему регистру.
    """
    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        return result.lower()


class Base64ImageField(serializers.ImageField):
    """
    Сохраняет изображение в base64.
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)
