from django.utils.functional import SimpleLazyObject
from django.utils.module_loading import import_string

from configfactory.configurations import settings
from configfactory.configurations.backends.base import ConfigBackend


backend = SimpleLazyObject(func=lambda: _get_backend())  # type: ConfigBackend


def get_settings(component, environment=None, flatten=False):
    return backend.get_settings(component, environment)


def update_settings(component, environment, settings):
    backend.update_settings(component, environment, settings)


def _get_backend():
    klass = import_string(settings.CONFIG_BACKEND['class'])
    options = settings.CONFIG_BACKEND.get('options', {})
    return klass(**options)
