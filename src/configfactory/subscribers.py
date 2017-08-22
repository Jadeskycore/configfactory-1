from django.core.cache import cache
from django.dispatch import receiver

from configfactory.services import backup
from configfactory.models import Component
from configfactory.signals import config_updated


@receiver(config_updated, sender=Component)
def config_updated_handler(sender, component, environment, **kwargs):

    # Create backup
    backup.create_backup()

    # Reset cache
    cache_key = 'settings:{}:{}'.format(
        component.alias,
        environment.alias
    )
    cache.delete(cache_key)
