import collections

from django.db import models
from django.conf import settings

from autoslug import AutoSlugField
from jsonfield import JSONField

from am.configfactory.utils import merge_dicts, flatten_dict, sort_dict


class Component(models.Model):

    name = models.CharField(max_length=64, unique=True)

    alias = AutoSlugField(populate_from='name')

    settings = JSONField(default={})

    settings_development = JSONField(default={})

    settings_staging = JSONField(default={})

    settings_production = JSONField(default={})

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

    def get_settings(self, environment=None, flatten=False, sort=False):

        if environment:
            try:
                env_settings = getattr(self, 'settings_{}'.format(environment))
            except AttributeError:
                env_settings = {}
            ret = merge_dicts(self.settings, env_settings)
        else:
            ret = self.settings

        if flatten:
            ret = flatten_dict(ret)

        if sort:
            ret = sort_dict(ret)

        return ret

    def get_all_settings(self, flatten=False):
        return collections.OrderedDict(
            [
                (
                    environment if environment is not None else 'base',
                    self.get_settings(environment, flatten=flatten)
                )
                for environment in [None] + settings.ENVIRONMENTS
            ]
        )
