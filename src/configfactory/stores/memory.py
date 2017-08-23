from typing import Dict

from .base import ConfigStore


class MemoryConfigStore(ConfigStore):

    def __init__(self):
        super().__init__()
        self.settings = {}  # type: Dict[str, dict]

    def all_impl(self):
        return self.settings

    def get_impl(self, component: str, environment: str) -> dict:
        try:
            return self.settings[component][environment]
        except KeyError:
            return {}

    def update_impl(self, component: str, environment: str, data: str):
        if component not in self.settings:
            self.settings[component] = {}
        self.settings[component][environment] = data
