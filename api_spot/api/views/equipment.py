from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from api.filters import SpotEquipmentFilter
from api.mixins import RetrieveListViewSet
from api.serializers import EquipmentGetSerializer
from spots.models import SpotEquipment


@extend_schema(
    tags=('equipments',)
)
class EquipmentViewSet(RetrieveListViewSet):
    """
    Представление оборудования по локациям с возможностью фильтрации
    по категориям.
    """
    queryset = SpotEquipment.objects.all()
    serializer_class = EquipmentGetSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = SpotEquipmentFilter
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Получение выборки с обородуванием."""
        location_id = self.kwargs.get('location_id')
        return super().get_queryset().filter(
            spot__location=location_id
        ).distinct('equipment')  # only postgers
