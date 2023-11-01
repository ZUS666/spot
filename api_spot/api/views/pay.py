import decimal

from django.db.models import F
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from api.exceptions import OrderStatusError
from api.permissions import IsOwnerOrReadOnly
from api.serializers.pay import PaySimpleSerializer
# from api.serializers.pay import PaySerializer
from api.services.orders import order_confirmation_email
from spots.constants import PAID, WAIT_PAY


@extend_schema(
    tags=('pay',),
)
class PayView(UpdateAPIView):
    """
    Оплачивание заказа(изменения статуса).
    """
    permission_classes = (IsOwnerOrReadOnly, )
    serializer_class = PaySimpleSerializer
    http_method_names = ('patch',)

    def patch(
            self, request, *args, **kwargs
    ) -> Response:
        """Метод patch, для оплачивания заказа."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        order = data.get('order')
        # order = get_object_or_404(
        #     Order,
        #     id=int(kwargs['order_id']),
        #     spot=int(kwargs['spot_id']),
        #     spot__location=int(kwargs['location_id'])
        # )
        self.check_object_permissions(request, order)
        if order.status != WAIT_PAY:
            raise OrderStatusError
        promocode = data.get('promocode')
        if promocode:
            order.bill *= decimal.Decimal(
                ((100 - promocode.percent_discount) / 100),
            )
            order.bill = order.bill.quantize(decimal.Decimal("1.00"))
            promocode.balance = F('balance') - 1
            promocode.save(update_fields=['balance'])

        order.status = PAID
        order.save(update_fields=['status', 'bill'])
        order_confirmation_email(order)
        return Response(
            {'message': 'Заказ оплачен'},
            status=status.HTTP_200_OK
        )
