from typing import Dict, Union

from configfactory.models import Config

from .base import ConfigStore


class DatabaseConfigStore(ConfigStore):

    def all_data(self) -> Dict[str, Dict[str, Union[str, bytes]]]:
        settings = {}  # type: Dict[str, Dict[str, str]]
        for config in Config.objects.all():
            if config.component not in settings:
                settings[config.component] = {}
            settings[config.component][config.environment] = config.data
        return settings

    def get_data(self, component: str, environment: str) -> Union[str, bytes]:
        config, created = Config.objects.get_or_create(
            component=component,
            environment=environment
        )
        return config.data

    def update_data(self, component: str, environment: str, data: str):
        config, created = Config.objects.get_or_create(
            component=component,
            environment=environment
        )
        config.data = data
        config.save(update_fields=['data'])
