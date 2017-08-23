from typing import Dict

from .base import ConfigStore


class MemoryConfigStore(ConfigStore):

    def __init__(self):
        super().__init__()
        self.settings = {}  # type: Dict[str, dict]

    def all_impl(self):
        return self.settings

    def get_impl(self, component: str, environment: str) -> dict:
        pass

    def update_impl(self, component: str, environment: str, data: str):
        pass
