from django.core.cache import caches


def get_settings_cache():
    return caches['settings']


def make_settings_key(component, environment=None):
    parts = ['settings']
    if component:
        parts.append('c:{}'.format(component))
    if environment:
        parts.append('e:{}'.format(environment))
    return '/'.join(parts)


def get_settings(component=None, environment=None):
    cache = get_settings_cache()
    key = make_settings_key(component, environment)
    return cache.get(key)


def set_settings(data, component=None, environment=None):
    cache = get_settings_cache()
    key = make_settings_key(component, environment)
    cache.set(key, data, timeout=60 * 60)


def delete_settings(component=None, environment=None):
    cache = get_settings_cache()
    key = make_settings_key(component, environment)
    cache.delete(key)
