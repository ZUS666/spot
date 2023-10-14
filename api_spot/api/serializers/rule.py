from rest_framework import serializers

from information.models import Rule


class RuleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода правил сервиса.
    """

    class Meta:
        model = Rule
        fields = (
            'id', 'title', 'text',
        )
