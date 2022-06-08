from django.core.validators import URLValidator
from rest_framework import serializers


class DefaultSchemaURLField(serializers.URLField):
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        if not any(value.startswith(f"{schema}://") for schema in URLValidator.schemes):
            return f"http://{value}"
        return value
