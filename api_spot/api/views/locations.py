from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from ..serializers import LocationsGetSerializer
from spots.models import Location


class LocationViewSet(RetrieveListViewSet):
    """
    Вьюсет для локаций.
    """
    queryset = Location.objects.all()
    serializer_class = LocationsGetSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
