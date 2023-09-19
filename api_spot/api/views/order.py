from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from api.mixins import CreateDestroyViewSet, RetrieveListViewSet
from api.permissions import IsOwnerOrReadOnly
from api.serializers.order import OrderSerializer
from spots.models.order import Order


class OrderViewSet(CreateDestroyViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class OrderGetViewSet(RetrieveListViewSet):
    """Вьюсет модели отзывов для получения."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Получение выборки с отзывами текущего коворкинга."""
        return super().get_queryset().filter(user=self.request.user)
