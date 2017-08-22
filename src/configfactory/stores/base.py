import abc


class ConfigStore(abc.ABC):

    @abc.abstractmethod
    def all(self):
        """
        Get all settings.
        """

    @abc.abstractmethod
    def get(self, component: str, environment: str) -> dict:
        """
        Get settings.
        """

    @abc.abstractmethod
    def update(self, component: str, environment: str, settings: dict):
        """
        Update settings.
        """
