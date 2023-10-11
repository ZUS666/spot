from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.mixins import CreateDestroyViewSet
from api.serializers.favorite import FavoriteSerializer
from spots.models.favorite import Favorite


@extend_schema(
    tags=('favorite',)
)
class FavoriteViewSet(CreateDestroyViewSet):
    """
    Добавление в избранное и удаление из избранного авторизованным
    пользователем.
    """
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.favorites.all()

    def delete(self, request, location_id):
        """Удаление избраного."""
        favorite = get_object_or_404(
            Favorite,
            user=request.user,
            location=location_id,
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
