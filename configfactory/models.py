import collections

from django.conf import settings
from django.db import models
from django.http import Http404
from jsonfield import JSONField

from configfactory.utils import (
    flatten_dict,
    json_dumps,
    json_loads,
    merge_dicts,
)


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

        if isinstance(environment, str):
            environment = environments.get(environment)

        if environment.is_base:
            ret = base_settings_dict
        else:
            env_settings_dict = settings_dict.get(environment.alias)
            if env_settings_dict is None:
                if environment.fallback:
                    env_settings_dict = settings_dict.get(
                        environment.fallback,
                        {}
                    )
                else:
                    env_settings_dict = {}
            ret = merge_dicts(
                base_settings_dict,
                env_settings_dict,
            )

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
                    environment.alias,
                    self.get_settings(environment, flatten=flatten)
                )
                for environment in environments
            ]
        )


class Environment:

    base_alias = 'base'

    def __init__(self, alias, name=None, fallback=None):
        if name is None:
            name = alias.title()
        self.alias = alias
        self.name = name
        self.fallback = fallback

    @property
    def is_base(self):
        return self.alias == self.base_alias

    def __str__(self):
        return self.alias


class EnvironmentHandler:

    def __init__(self):
        self._environments = collections.OrderedDict([
            (
                Environment.base_alias,
                Environment(
                    alias=Environment.base_alias,
                    name='Base'
                )
            )
        ])
        for environment in getattr(settings, 'ENVIRONMENTS', []):
            alias = environment['alias']
            name = environment.get('name')
            fallback = environment.get('fallback')
            self._environments[alias] = Environment(
                alias=alias,
                name=name,
                fallback=fallback
            )

    def get(self, alias=None):
        if alias is None:
            alias = Environment.base_alias
        return self._environments[alias]

    def get_or_404(self, alias=None):
        try:
            return self.get(alias)
        except KeyError:
            raise Http404

    def __contains__(self, item):
        return item is self._environments

    def __getitem__(self, item):
        return self.get(item)

    def __iter__(self):
        for environment in self._environments.values():
            yield environment


environments = EnvironmentHandler()
