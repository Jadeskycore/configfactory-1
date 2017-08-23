from django.dispatch import receiver

from configfactory import cache
from configfactory.models import Component, Environment
from configfactory.services import backup
from configfactory.signals import component_deleted, config_updated


@receiver(config_updated, sender=Component)
def config_updated_handler(sender, component, environment, **kwargs):

    # Create backup
    backup.create_backup()

    # Reset component cache
    cache.delete_settings(environment=environment.alias)
    cache.delete_settings(
        component=component.alias,
        environment=environment.alias
    )


@receiver(component_deleted, sender=Component)
def component_deleted_handler(sender, component, **kwargs):

    # Reset component cache
    for environment in Environment.objects.all():
        cache.delete_settings(environment=environment.alias)
        cache.delete_settings(
            component=component.alias,
            environment=environment.alias
        )
