from drf_spectacular.utils import extend_schema
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated


from api.services.orders import order_finished_email
from api.serializers.pay import PaySerializer
from spots.constants import PAID
from spots.models import Order


@extend_schema(
    tags=('pay',)
)
class PayView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = PaySerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('put',)

    def get_queryset(self):
        """Получение выборки с заказами для текущего пользователя."""
        order_id = self.kwargs.get('order_id')
        spot_id, = self.kwargs.get('spot_id,')
        location_id = self.kwargs.get('location_id')

        return super().get_queryset().filter(
            pk=order_id,
            spot=spot_id,
            user=self.request.user,
            spot__location=location_id,
        )

    def perform_update(self, serializer):
        """Подверждения оплаты."""
        order = serializer.order
        order.status = PAID
        order.save()
        order_finished_email(order)
