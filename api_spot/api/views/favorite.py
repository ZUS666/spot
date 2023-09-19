from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from api.mixins import CreateDestroyViewSet
from api.serializers.favorite import FavoriteSerializer
from spots.models.favorite import Favorite


class FavoriteViewSet(CreateDestroyViewSet):
    """Вьюсет для избранного."""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
