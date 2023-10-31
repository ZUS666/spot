from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers.promocode_check import PromocodeCheckSerializer


@extend_schema(
    tags=('pay',),
)
class PromocodeCheckAPIView(CreateAPIView):
    """
    Представление доступности проверки промокода.
    """
    serializer_class = PromocodeCheckSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        promocode = serializer.validated_data.get('promocode')
        discount = promocode.percent_discount
        return Response(
            {'message': f'Промокод доступен на скидку {discount} %'},
            status=status.HTTP_200_OK,
        )
