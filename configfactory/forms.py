import jsonschema
from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields

from configfactory.exceptions import JSONEncodeError
from configfactory.models import Component
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


class ComponentForm(forms.ModelForm):

    class Meta:

        model = Component
        fields = ('name', 'alias', 'require_schema', 'is_global')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'alias': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }


class ComponentSettingsForm(forms.Form):

    def __init__(self, schema=None, require_schema=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if schema is None:
            schema = {}
        self.require_schema = require_schema
        self.schema = schema

    settings = JSONFormField(required=False, widget=forms.Textarea(attrs={
        'rows': 32,
        'style': 'width: 100%',
    }))

    def clean_settings(self):
        data = self.cleaned_data['settings']
        if self.require_schema:
            try:
                jsonschema.validate(data, self.schema)
            except jsonschema.ValidationError as e:
                raise ValidationError(str(e))
        return data


class ComponentSchemaForm(forms.Form):

    schema = JSONFormField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 32,
            'style': 'width: 100%',
        })
    )
