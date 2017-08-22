from django.core.cache import cache
from django.dispatch import receiver

from configfactory.models import Component
from configfactory.signals import config_updated


@receiver([
    config_updated
], sender=Component)
def reset_component_cache(sender, component, environment, **kwargs):
    cache_key = 'settings:{}:{}'.format(
        component.alias,
        environment.alias
    )
    cache.delete(cache_key)
