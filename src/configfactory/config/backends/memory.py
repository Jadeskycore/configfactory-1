from .base import ConfigBackend


class MemoryConfigBackend(ConfigBackend):

    def __init__(self):
        self.store = {}

    def get_settings(self, component, environment):
        try:
            return self.store[component][environment]
        except KeyError:
            return {}

    def update_settings(self, component, environment, settings):
        if component not in self.store:
            self.store[component] = {}
        self.store[component][environment] = settings
