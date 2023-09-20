
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
        return get_object_or_404(
            Spot,
            id=int(
                serializer_field.context.get('view').kwargs.get('spot_id')
            )
        )
 

class GetOrder(serializers.CurrentUserDefault):
    """Получение Order из view."""
    def __call__(self, serializer_field):
        return get_object_or_404(
            Order,
            id=int(
                serializer_field.context.get('view').kwargs.get('order_id')
            )
        )

class LowercaseEmailField(serializers.EmailField):
    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        return result.lower()
