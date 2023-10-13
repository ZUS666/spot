from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from api.serializers import RuleSerializer
from core.models import Rule


@extend_schema(
    tags=('rules',)
)
class RuleViewSet(RetrieveListViewSet):
    """
    Представление для вывода правил сервиса.
    """
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = (AllowAny,)
