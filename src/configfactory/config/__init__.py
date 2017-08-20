from django.utils.functional import LazyObject
from django.utils.module_loading import import_string

from configfactory.config import settings
from configfactory.config.backends.base import ConfigBackend


class ConfigBackendProxy(LazyObject):

    default = 'configfactory.config.backends.memory.MemoryBackendConfig'

    def _setup(self):
        klass = import_string(settings.CONFIG_BACKEND['CLASS'])
        options = settings.CONFIG_BACKEND.get('OPTIONS', {})
        self._wrapped = klass(**options)


backend = ConfigBackendProxy()  # type: ConfigBackend


def get_settings(component, environment):
    return backend.get_settings(component, environment)


def update_settings(component, environment, settings):
    backend.update_settings(component, environment, settings)


default_app_config = 'configfactory.config.apps.ConfigConfig'
