from rest_framework import serializers

from information.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода частозадваемых вопросов.
    """

    class Meta:
        model = Question
        fields = (
            'id', 'question', 'answer', 'icon'
        )
