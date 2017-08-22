from .base import ConfigStore


class FileConfigStore(ConfigStore):

    def all(self):
        pass

    def get(self, component: str, environment: str) -> dict:
        pass

    def update(self, component: str, environment: str, settings: dict):
        pass
