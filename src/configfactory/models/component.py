from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from configfactory.utils import json_dumps, json_loads


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

    schema_json = models.TextField(
        blank=True,
        null=True,
        default='{}'
    )

    require_schema = models.BooleanField(
        default=True,
        help_text='Use json schema validation'
    )

    is_global = models.BooleanField(
        default=False,
        help_text="Use only base environment"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('creation datetime')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('modification datetime')
    )

    class Meta:
        verbose_name = _('component')
        verbose_name_plural = _('components')
        ordering = ('name',)

    def __str__(self):
        return self.name

    @cached_property
    def settings(self):
        return json_loads(self.settings_json)

    @property
    def schema(self):
        return json_loads(self.schema_json)

    @schema.setter
    def schema(self, value):
        self.schema_json = json_dumps(value)

    @property
    def cache_key(self):
        return 'settings:{}'.format(self.alias)
