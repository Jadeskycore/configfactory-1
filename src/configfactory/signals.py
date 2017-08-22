from django.dispatch import Signal

config_updated = Signal(providing_args=['component', 'environment'])