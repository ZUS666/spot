import datetime

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


from api.mixins import CreateDestroyViewSet, RetrieveListViewSet
from api.permissions import IsOwnerOrReadOnly
from api.serializers.order import OrderSerializer
from spots.models import Order
from api.tasks import change_status_task, close_status_task


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
        finish_time = instance.date_finish
        countdown = (finish_time - datetime.datetime.now()).total_seconds()
        print(countdown)
        # close_status_task.apply_async(
        #     args=[instance.id], countdown=countdown
        # )


class OrderGetViewSet(RetrieveListViewSet):
    """Вьюсет модели заказов для получения."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Получение выборки с заказами для текущего пользователя."""
        if self.request.user.is_authenticated:
            return super().get_queryset().filter(user=self.request.user)
        return super().get_queryset()
