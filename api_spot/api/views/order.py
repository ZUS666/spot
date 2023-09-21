from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


from api.mixins import CreateDestroyViewSet, RetrieveListViewSet
from api.permissions import IsOwnerOrReadOnly
from api.serializers.order import OrderSerializer

from spots.models import Order
from api.tasks import change_status_task



class OrderViewSet(CreateDestroyViewSet):
    """Вьюсет для заказов."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        instance = serializer.save()
        # change_status_task.apply_async(
        #     args=[instance.id], countdown=settings.TIME_CHANGE_STATUS
        # )


class OrderGetViewSet(RetrieveListViewSet):
    """Вьюсет модели отзывов для получения."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Получение выборки с отзывами текущего коворкинга."""
        if self.request.user.is_authenticated:
            return super().get_queryset().filter(user=self.request.user)
        return super().get_queryset()
