from typing import Dict, Union

from .base import ConfigStore


class MemoryConfigStore(ConfigStore):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._settings = {}  # type: Dict[str, Dict[str, str]]

    def all_data(self) -> Dict[str, Dict[str, Union[str, bytes]]]:
        return self._settings

    def get_data(self, environment: str, component: str) -> Union[str, bytes]:
        try:
            return self._settings[environment][component]
        except KeyError:
            return ''

    def update_data(self, environment: str, component: str, data: str):
        if environment not in self._settings:
            self._settings[environment] = {}
        self._settings[environment][component] = data
