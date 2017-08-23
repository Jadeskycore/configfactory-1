from typing import Dict, Union

from .base import ConfigStore


class FileConfigStore(ConfigStore):

    def all_data(self) -> Dict[str, Dict[str, Union[str, bytes]]]:
        pass

    def get_data(self, environment: str, component: str) -> Union[str, bytes, None]:
        pass

    def update_data(self, environment: str, component: str, data: str):
        pass
