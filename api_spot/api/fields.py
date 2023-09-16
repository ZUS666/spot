from django.shortcuts import get_object_or_404
from rest_framework import serializers

from spots.models.location import Location


class GetLocation(serializers.CurrentUserDefault):
    """Получение локации из view."""
    def __call__(self, serializer_field):
        return get_object_or_404(
            Location,
            id=int(
                serializer_field.context.get('view').kwargs.get('location_id')
            )
        )
