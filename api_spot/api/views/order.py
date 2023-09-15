from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from api.mixins import CreateDestroyViewSet, RetrieveListViewSet
from api.serializers.order import OrderSerializer

from spots.models.order import Order
from spots.models.spot import Spot


class OrderViewSet(CreateDestroyViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_spot(self):
        """Получение текущего объекта (коворкинга)."""
        return get_object_or_404(Spot, pk=self.kwargs.get("spot_id"))

    def perform_create(self, serializer):
        """Создание брони для текущего коворкинга."""
        serializer.save(
            user=self.request.user,
            spot=self.get_spot()
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["spot_id"] = self.kwargs.get("spot_id")
        return context


class OrderGetViewSet(RetrieveListViewSet):
    """Вьюсет модели отзывов для получения."""
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Получение выборки с отзывами текущего коворкинга."""
        return Order.objects.filter(user=self.request.user)
