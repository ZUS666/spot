from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from api.serializers import RuleSerializer
from spots.models import Rule


class RuleViewSet(RetrieveListViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = (AllowAny,)
