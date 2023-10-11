from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from api.filters import LocationFilter
from api.mixins import RetrieveListViewSet
from api.paginations import FourPageNumberPagination, SixPageNumberPagination
from api.serializers import LocationGetSerializer, LocationGetShortSerializer
from spots.models import Location


class LocationViewSet(RetrieveListViewSet):
    """
    Представление подробной информации о локациях с возможностью фильтрации
    по названию, категориям, метро и избранному.
    """
    queryset = Location.objects.all()
    serializer_class = LocationGetSerializer
    permission_classes = (AllowAny,)
    pagination_class = FourPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LocationFilter


@extend_schema(
    tags=('locations',)
)
class LocationShortListAPIView(ListAPIView):
    """
    Представление краткой информации о локациях с возможностью фильтрации
    по названию, категориям, метро и избранному и поиску по названию.
    """
    queryset = Location.objects.all()
    serializer_class = LocationGetShortSerializer
    permission_classes = (AllowAny,)
    pagination_class = SixPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = LocationFilter
    search_fields = ('^name',)
