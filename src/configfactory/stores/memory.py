from typing import Dict

from .base import ConfigStore


class MemoryConfigStore(ConfigStore):

    def __init__(self):
        self.settings = {}  # type: Dict[str, dict]

    def get(self, component: str, environment: str) -> dict:
        """
        Get settings.
        """

    def update(self, component: str, environment: str, settings: dict):
        """
        Update settings.
        """
