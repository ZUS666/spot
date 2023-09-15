from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


from api.mixins import CreateDestroyViewSet
from api.serializers.favorite import FavoriteSerializer

from spots.models.location import Location


class FavoriteViewSet(CreateDestroyViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_location(self):
        """Получение текущего объекта (локации)."""
        return get_object_or_404(Location, pk=self.kwargs.get("location_id"))

    def perform_create(self, serializer):
        """Создание избранного для текущей локации."""
        serializer.save(
            user=self.request.user,
            location=self.get_location()
        )
