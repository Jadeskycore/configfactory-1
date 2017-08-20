from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConfigConfig(AppConfig):

    name = 'configfactory.config'
    verbose_name = _("Configuration manager")

    def ready(self):
        pass
