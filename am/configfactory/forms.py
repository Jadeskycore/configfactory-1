import json

from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError

from am.configfactory.models import Component


class JSONFormField(fields.CharField):

    def to_python(self, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except ValueError:
                raise ValidationError("Enter valid JSON")
        return value

    def clean(self, value):

        if not value and not self.required:
            return None

        try:
            return super().clean(value)
        except TypeError:
            raise ValidationError("Enter valid JSON")


class ComponentForm(forms.ModelForm):

    name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Component
        fields = ('name', )


class ComponentSettingsForm(forms.Form):

    settings = JSONFormField(required=False, widget=forms.Textarea(attrs={
        'rows': 32,
        'style': 'width: 100%',
    }))
