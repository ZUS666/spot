from rest_framework import serializers

from spots.models import Rule


class RuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rule
        fields = (
            'id', 'title', 'text',
        )
