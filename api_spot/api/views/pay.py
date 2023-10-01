from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.services.orders import order_finished_email
from api.serializers.pay import PaySerializer
from api.permissions import IsOwnerOrReadOnly
from spots.constants import PAID, WAIT_PAY
from spots.models import Order


@extend_schema(
    tags=('pay',),
    request=PaySerializer
)
class PayView(APIView):
    permission_classes = (IsOwnerOrReadOnly, )

    def patch(self, request, location_id, spot_id, order_id):
        serializer = PaySerializer(
            data=request.data,
            context={'order_id': order_id}
        )
        if serializer.is_valid():
            order = get_object_or_404(
                Order, pk=order_id,
                spot=spot_id,
                spot__location=location_id,
            )
            self.check_object_permissions(request, order)
            if order.status != WAIT_PAY:
                return Response(
                    'Нельзя оплачивать',
                    status=status.HTTP_400_BAD_REQUEST
                )
            order.status = PAID
            order.save()
            order_finished_email(order)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
