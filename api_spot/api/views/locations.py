from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from ..serializers import LocationsGetSerializer
from spots.models import Location
from api.filters import LocationFilter


class LocationViewSet(RetrieveListViewSet):
    """
    Вьюсет для локаций.
    """
    queryset = Location.objects.all()
    serializer_class = LocationsGetSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LocationFilter
    pagination_class = PageNumberPagination
