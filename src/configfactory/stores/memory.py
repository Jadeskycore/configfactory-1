from typing import Dict, Union

from .base import ConfigStore


class MemoryConfigStore(ConfigStore):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._settings = {}  # type: Dict[str, Dict[str, str]]

    def all_data(self) -> Dict[str, Dict[str, Union[str, bytes]]]:
        return self._settings

    def get_data(self, component: str, environment: str) -> Union[str, bytes]:
        try:
            return self._settings[component][environment]
        except KeyError:
            return ''

    def update_data(self, component: str, environment: str, data: str):
        if component not in self._settings:
            self._settings[component] = {}
        self._settings[component][environment] = data
