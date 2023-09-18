from rest_framework import serializers


class LowercaseEmailField(serializers.EmailField):
    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        return result.lower()
