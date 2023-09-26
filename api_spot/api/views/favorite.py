from rest_framework.pagination import PageNumberPagination

from api.mixins import CreateDestroyViewSet
from api.serializers.favorite import FavoriteSerializer
from spots.models.favorite import Favorite
from api.permissions import IsOwnerOrReadOnly


class FavoriteViewSet(CreateDestroyViewSet):
    """Вьюсет для избранного."""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = PageNumberPagination
