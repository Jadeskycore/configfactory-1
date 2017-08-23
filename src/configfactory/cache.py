from typing import Optional

from django.core.cache import BaseCache, caches


def get_settings_cache() -> BaseCache:
    return caches['settings']


def make_settings_key(component: str, environment: str = None):
    parts = ['settings']
    if component:
        parts.append('c:{}'.format(component))
    if environment:
        parts.append('e:{}'.format(environment))
    return '/'.join(parts)


def get_settings(component: str = None, environment: str = None) -> Optional[dict]:
    cache = get_settings_cache()
    key = make_settings_key(component, environment)
    return cache.get(key)


def set_settings(data: dict, component: str = None, environment: str = None):
    cache = get_settings_cache()
    key = make_settings_key(component, environment)
    cache.set(key, data, timeout=60 * 60)


def delete_settings(component: str = None, environment: str = None):
    cache = get_settings_cache()
    key = make_settings_key(component, environment)
    cache.delete(key)
