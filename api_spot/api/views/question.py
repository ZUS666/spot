from rest_framework.permissions import AllowAny

from api.mixins import RetrieveListViewSet
from api.serializers import QuestionSerializer
from spots.models import Question


class QuestionViewSet(RetrieveListViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (AllowAny,)
