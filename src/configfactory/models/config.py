from typing import Union

from django.db import models
from django.utils.translation import ugettext_lazy as _

from configfactory.utils import json_dumps, json_loads


class Config(models.Model):

    component = models.SlugField(
        verbose_name=_('component alias')
    )

    environment = models.SlugField(
        verbose_name=_('environment alias')
    )

    settings_json = models.TextField(
        blank=True,
        null=True,
        default='{}'
    )

    class Meta:
        verbose_name = _('config')
        verbose_name_plural = _('configs')
        unique_together = ('component', 'environment')

    @property
    def settings(self) -> dict:
        return json_loads(self.settings_json)

    @settings.setter
    def settings(self, val: Union[dict, str]):
        if isinstance(val, str):
            self.settings_json = val
        elif isinstance(val, dict):
            self.settings_json = json_dumps(val)
