from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from api.serializers import EventSerializer
from spots.models import Event
from rest_framework.pagination import LimitOffsetPagination


@extend_schema(
    tags=('events',)
)
class EventViewSet(RetrieveListViewSet):
    """
    Представление для вывода мероприятий.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
