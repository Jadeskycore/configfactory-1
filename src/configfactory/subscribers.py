from django.dispatch import receiver

from configfactory.models import Component
from configfactory.services import backup
from configfactory.signals import component_deleted, config_updated


@receiver(config_updated, sender=Component)
def config_updated_handler(sender, component, environment, **kwargs):

    # Create backup
    backup.create_backup()


@receiver(component_deleted, sender=Component)
def component_deleted_handler(sender, component, **kwargs):
    pass
