from .base import ConfigStore


class DatabaseConfigStore(ConfigStore):

    def get_settings(self, component, environment):
        pass

    def update_settings(self, component, environment, settings):
        pass
