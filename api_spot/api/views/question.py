from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from api.serializers import QuestionSerializer
from information.models import Question


@extend_schema(
    tags=('questions',)
)
class QuestionViewSet(RetrieveListViewSet):
    """
    Представление для вывода частозадаваемых вопросов.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (AllowAny,)
