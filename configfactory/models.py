import collections

from django.conf import settings
from django.db import models
from jsonfield import JSONField

from configfactory.utils import flatten_dict, merge_dicts, json_loads, json_dumps


class Component(models.Model):

    name = models.CharField(max_length=64, unique=True)

    alias = models.SlugField(
        unique=True,
        help_text='Unique component alias'
    )

    settings_json = models.TextField(
        blank=True,
        null=True,
        default='{}'
    )

    schema = JSONField(default={})

    require_schema = models.BooleanField(
        default=True,
        help_text='Use json schema validation'
    )

    is_global = models.BooleanField(
        default=False,
        help_text="Use only base environment"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_settings(self, environment=None, flatten=False, raw_json=False):

        settings_dict = json_loads(self.settings_json)
        base_settings_dict = settings_dict.get(
            Environment.base_alias,
            {}
        )

        if environment:
            env_settings_dict = settings_dict.get(environment, {})
            ret = merge_dicts(
                base_settings_dict,
                env_settings_dict,
            )
        else:
            ret = base_settings_dict

        if flatten:
            ret = flatten_dict(ret)

        if raw_json:
            return json_dumps(ret, indent=4)

        return ret

    def set_settings(self, data, environment=None):

        if environment is None:
            environment = Environment.base_alias

        settings_dict = json_loads(self.settings_json)

        if isinstance(data, str):
            data = json_loads(data)

        settings_dict[environment] = data

        self.settings_json = json_dumps(settings_dict)

    def get_all_settings(self, flatten=False):
        return collections.OrderedDict(
            [
                (
                    environment or Environment.base_alias,
                    self.get_settings(environment, flatten=flatten)
                )
                for environment in [None] + settings.ENVIRONMENTS
            ]
        )


class Environment:

    base_alias = 'base'

    def __init__(self):
        pass
