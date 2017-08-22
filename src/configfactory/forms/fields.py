from django.core.exceptions import ValidationError
from django.forms import fields

from configfactory.exceptions import JSONEncodeError
from configfactory.utils import json_dumps, json_loads


class JSONFormField(fields.CharField):

    def to_python(self, value):
        if isinstance(value, str):
            try:
                return json_loads(value)
            except JSONEncodeError:
                raise ValidationError("Enter valid JSON")
        return value

    def clean(self, value):
        if not value and not self.required:
            return None
        try:
            return super().clean(value)
        except TypeError:
            raise ValidationError("Enter valid JSON")

    def prepare_value(self, value):
        if isinstance(value, dict):
            return json_dumps(value, indent=4)
        return value
