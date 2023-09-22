from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from ..serializers import SpotSerializer
from spots.models import Spot


class SpotViewSet(RetrieveListViewSet):
    """
    Вьюсет для локаций.
    """
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        location_id = self.kwargs.get('location_id')
        return super().get_queryset().filter(location_id=location_id)
