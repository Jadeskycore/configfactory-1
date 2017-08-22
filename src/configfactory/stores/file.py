from .base import ConfigStore


class FileConfigStore(ConfigStore):

    def get(self, component: str, environment: str) -> dict:
        """
        Get settings.
        """

    def update(self, component: str, environment: str, settings: dict):
        """
        Update settings.
        """
