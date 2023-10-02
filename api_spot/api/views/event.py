from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from api.serializers import EventSerializer
from spots.models import Event


class EventViewSet(RetrieveListViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)
