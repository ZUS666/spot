from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers.pay import PaySerializer


@api_view(['POST'])
def confirmation_pay(request, location_id, spot_id, order_id):
    """Подверждения оплаты."""
    serializer = PaySerializer(data=request.data)
    if serializer.is_valid():
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
