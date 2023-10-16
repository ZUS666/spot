from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from api.filters import OrderFilter
from api.mixins import CreateUpdateViewSet, RetrieveListViewSet
from api.permissions import IsOwnerOrReadOnly
from api.serializers.order import (
    OrderGetSerializer, OrderSerializer, OrderUpdateSerializer,
)
from api.services.orders import order_cancel_email, order_confirmation_email
from api.tasks import change_status_task
from spots.constants import CANCEL, PAID, WAIT_PAY
from spots.models import Order


@extend_schema(
    tags=('orders',)
)
class OrderViewSet(CreateUpdateViewSet):
    """
    Представление создания заказов и изменение статуса для отмены.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    http_method_names = ('post', 'patch')

    def get_serializer_class(self):
        if self.action == 'update':
            return OrderUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        instance = serializer.save()
        change_status_task.apply_async(
            args=[instance.id], countdown=settings.TIME_CHANGE_STATUS
        )
        order_confirmation_email(instance)

    def partial_update(self, serializer):
        instance = serializer.instance
        if instance.status == PAID:
            instance.status = CANCEL
            instance.save()
            order_cancel_email(instance)
        if instance.status == WAIT_PAY:
            instance.status = CANCEL
            instance.save()


class OrderGetViewSet(RetrieveListViewSet):
    """
    Представление заказов авторизованного пользователя с возможностью
    фильтрации по статусу "завершен".
    """
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = OrderFilter
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Получение выборки с заказами для текущего пользователя."""
        return super().get_queryset().filter(user=self.request.user)
