from typing import Dict

from configfactory.models import Config

from .base import ConfigStore


class DatabaseConfigStore(ConfigStore):

    def all_impl(self) -> Dict[str, Dict[str, str]]:
        settings = {}  # type: Dict[str, Dict[str, str]]
        for config in Config.objects.all():
            if config.component not in settings:
                settings[config.component] = {}
            settings[config.component][config.environment] = config.settings_json
        return settings

    def get_impl(self, component: str, environment: str) -> str:
        config, created = Config.objects.get_or_create(
            component=component,
            environment=environment
        )
        return config.settings_json

    def update_impl(self, component: str, environment: str, data: str):
        config, created = Config.objects.get_or_create(
            component=component,
            environment=environment
        )
        config.settings_json = data
        config.save(update_fields=['settings_json'])
