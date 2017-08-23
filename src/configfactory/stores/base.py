import abc
from typing import Dict, Union

from configfactory.utils import json_dumps, json_loads


class ConfigStore(abc.ABC):

    def __init__(self, encode_key: str = None, encode_enabled: bool = False):
        self.encode_key = encode_key
        self.encode_enabled = encode_enabled

    def all(self) -> dict:
        """
        Get all settings.
        """
        all_settings = {}
        for environment, component_data in self.all_impl().items():
            all_settings[environment] = {}
            for component, data in component_data.items():
                settings = json_loads(self._decode(data))
                all_settings[environment][component] = settings
        return all_settings

    def get(self, component: str, environment: str) -> dict:
        """
        Get settings.
        """
        settings = self.get_impl(component, environment)
        return json_loads(settings)

    def update(self, component: str, environment: str, settings: dict):
        """
        Update settings.
        """
        # Prepare settings string
        if isinstance(settings, dict):
            settings = json_dumps(settings)
        data = self._encode(settings)
        self.update_impl(component, environment, data)

    @abc.abstractmethod
    def all_impl(self) -> Dict[str, Dict[str, str]]:
        pass

    @abc.abstractmethod
    def get_impl(self, component: str, environment: str) -> Union[str, dict]:
        pass

    @abc.abstractmethod
    def update_impl(self, component: str, environment: str, data: str):
        pass

    def _encode(self, data: str) -> str:
        return data

    def _decode(self, data: str) -> str:
        return data
