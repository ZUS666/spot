from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination

from api.mixins import CreateDestroyViewSet
from api.permissions import IsOwnerOrReadOnly
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
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = PageNumberPagination
