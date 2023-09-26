from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from api.mixins import RetrieveListViewSet
from ..serializers import LocationGetSerializer, LocationGetShortSerializer
from spots.models import Location


class LocationViewSet(RetrieveListViewSet):
    """
    Вьюсет подбродной информации для локаций.
    """
    queryset = Location.objects.all()
    serializer_class = LocationGetSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination


class LocationShortListAPIView(ListAPIView):
    """
    Представление краткой информации о локациях.
    """
    queryset = Location.objects.all()
    serializer_class = LocationGetShortSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
