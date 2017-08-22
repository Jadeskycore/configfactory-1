from configfactory.models import Config

from .base import ConfigStore


class DatabaseConfigStore(ConfigStore):

    def get(self, component: str, environment: str) -> dict:
        """
        Get settings.
        """
        config, created = Config.objects.get_or_create(
            component=component
        )
        return config.settings.get(environment, {})

    def update(self, component: str, environment: str, settings: dict):
        """
        Update settings.
        """
        config, created = Config.objects.get_or_create(
            component=component
        )

        update_settings = config.settings.copy()
        update_settings[environment] = settings

        config.settings = update_settings
        config.save(update_fields=['settings_json'])
