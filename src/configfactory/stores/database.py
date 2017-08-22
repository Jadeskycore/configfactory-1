from configfactory.models import Config

from .base import ConfigStore


class DatabaseConfigStore(ConfigStore):

    def all(self):
        settings = {}
        for config in Config.objects.all():
            if config.component not in settings:
                settings[config.component] = settings
            settings[config.component][config.environment] = settings
        return settings

    def get(self, component: str, environment: str) -> dict:
        config, created = Config.objects.get_or_create(
            component=component,
            environment=environment
        )
        return config.settings

    def update(self, component: str, environment: str, settings: dict):
        config, created = Config.objects.get_or_create(
            component=component,
            environment=environment
        )
        config.settings = settings
        config.save(update_fields=['settings_json'])
