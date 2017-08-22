from typing import Dict

from .base import ConfigStore


class MemoryConfigStore(ConfigStore):

    def __init__(self):
        self.settings = {}  # type: Dict[str, dict]

    def all(self):
        return self.settings

    def get(self, component: str, environment: str) -> dict:
        pass

    def update(self, component: str, environment: str, settings: dict):
        pass
