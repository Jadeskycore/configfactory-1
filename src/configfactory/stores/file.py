from typing import Dict, Union

from .base import ConfigStore


class FileConfigStore(ConfigStore):

    def all_impl(self) -> Dict[str, Dict[str, Union[str, bytes]]]:
        pass

    def get_impl(self, component: str, environment: str) -> Union[str, bytes]:
        pass

    def update_impl(self, component: str, environment: str, data: str):
        pass
