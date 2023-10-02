from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.services.orders import order_finished_email
from api.serializers.pay import PaySerializer
from api.permissions import IsOwnerOrReadOnly
from spots.constants import PAID, WAIT_PAY


@extend_schema(
    tags=('pay',),
    request=PaySerializer
)
class PayView(APIView):
    """
    Оплачивание заказа(изменения статуса).
    """
    permission_classes = (IsOwnerOrReadOnly, )

    def patch(self, request, location_id, spot_id, order_id):
        serializer = PaySerializer(
            data=request.data,
            context={'order_id': order_id}
        )
        if serializer.is_valid(raise_exception=True):
            order = serializer.validated_data.get('order')
            self.check_object_permissions(request, order)
            if order.status != WAIT_PAY:
                return Response(
                    'Можно оплачить только заказы со статусом '
                    '"ожидается оплата"',
                    status=status.HTTP_400_BAD_REQUEST
                )
            order.status = PAID
            order.save()
            order_finished_email(order)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
