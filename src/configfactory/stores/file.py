from typing import Dict

from .base import ConfigStore


class FileConfigStore(ConfigStore):

    def all_impl(self) -> Dict[str, Dict[str, str]]:
        pass

    def get_impl(self, component: str, environment: str) -> str:
        pass

    def update_impl(self, component: str, environment: str, data: str):
        pass
