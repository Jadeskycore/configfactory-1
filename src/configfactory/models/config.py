from django.db import models
from django.utils.translation import ugettext_lazy as _


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
