from rest_framework import serializers

from spots.models import Question


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id', 'question', 'answer',
        )
