from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.services.orders import order_finished_email
from api.serializers.pay import PaySerializer
from spots.constants import PAID
from spots.models import Order


@extend_schema(
    tags=('pay',)
)
@api_view(['PATCH'])
@permission_classes((IsAuthenticated, ))
def confirmation_pay(request, location_id, spot_id, order_id):
    """Подверждения оплаты."""
    serializer = PaySerializer(data=request.data)
    if serializer.is_valid():
        order = get_object_or_404(
            Order, pk=order_id,
            spot=spot_id,
            spot__location=location_id,
        )
        if order.user != request.user:
            return Response('КТО ТЫ ВОИН?', status=status.HTTP_403_FORBIDDEN)
        order.status = PAID
        order.save()
        order_finished_email(order)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
