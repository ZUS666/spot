from api.mixins import CreateDestroyViewSet
from api.permissions import IsOwnerOrReadOnly
from api.serializers.favorite import FavoriteSerializer
from rest_framework.pagination import PageNumberPagination
from spots.models.favorite import Favorite


class FavoriteViewSet(CreateDestroyViewSet):
    """Вьюсет для избранного."""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = PageNumberPagination
