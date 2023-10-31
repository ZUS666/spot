from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.serializers.promocode_check import PromocodeCheckSerializer


@extend_schema(
    tags=('pay',),
)
class PromocodeCheckAPIView(CreateAPIView):
    serializer_class = PromocodeCheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'message': 'Промокод доступен'}, status=status.HTTP_200_OK
        )
