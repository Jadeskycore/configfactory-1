import jsonschema
from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields
from django.utils.html import format_html

from configfactory.exceptions import (
    CircularInjectError,
    InjectKeyError,
    JSONEncodeError,
)
from configfactory.models import Component
from configfactory.services import config
from configfactory.utils import inject_dict_params, json_dumps, json_loads


def html_params(**kwargs):
    params = []
    for k, v in sorted(kwargs.items()):
        if k in ('class_', 'class__', 'for_'):
            k = k[:-1]
        elif k.startswith('data_'):
            k = k.replace('_', '-', 1)
        if v is True:
            params.append(k)
        elif v is False:
            pass
        else:
            params.append('%s=%s' % (str(k), format_html(v)))
    return ' '.join(params)


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

    def __init__(self, component, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.component = component
        self.environment = environment

    settings = JSONFormField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 32,
            'style': 'width: 100%',
        })
    )

    def clean_settings(self):
        data = self.cleaned_data['settings']
        try:
            inject_dict_params(
                data=data,
                params=config.get_all_settings(self.environment, flatten=True),
                flatten=True,
                raise_exception=True
            )
        except (InjectKeyError, CircularInjectError) as e:
            raise ValidationError(str(e))
        if self.component.require_schema:
            try:
                jsonschema.validate(data, self.component.schema)
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
