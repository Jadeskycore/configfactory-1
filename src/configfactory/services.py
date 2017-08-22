from collections import OrderedDict

from django.core.cache import cache
from django.conf import settings
from django.db import transaction
from django.utils.functional import SimpleLazyObject
from django.utils.module_loading import import_string

from configfactory.exceptions import ComponentDeleteError, InjectKeyError
from configfactory.models import Component, Environment
from configfactory.shortcuts import get_environment_alias
from configfactory.signals import config_updated
from configfactory.stores.base import ConfigStore
from configfactory.utils import flatten_dict, inject_dict_params, merge_dicts

store = SimpleLazyObject(func=lambda: _init_store())  # type: ConfigStore


def get_settings(component: Component,
                 environment: Environment=None,
                 flatten: bool=False):
    """
    Get component settings.
    """

    cache_key = 'settings:{}:{}'.format(
        component.alias,
        environment.alias,
    )
    ret = cache.get(cache_key)

    if ret is None:

        if environment is None:
            environment = Environment.objects.base().get()

        if environment.is_base:
            ret = store.get(
                component=component.alias,
                environment=environment.alias
            )
        else:
            base_settings_dict = store.get(
                component=component.alias,
                environment=get_environment_alias()
            )
            env_settings_dict = store.get(
                component=component.alias,
                environment=environment.alias
            )
            if env_settings_dict is None:
                if environment.fallback_id:
                    env_settings_dict = store.get(
                        component=component.alias,
                        environment=environment.fallback.alias,
                    )
                else:
                    env_settings_dict = {}

            ret = merge_dicts(
                base_settings_dict,
                env_settings_dict,
            )

        cache.set(cache_key, ret, timeout=60 * 60)

    if flatten:
        ret = flatten_dict(ret)

    return ret


def get_all_settings(environment: Environment, flatten=False):
    """
    Get all settings.
    """
    data = OrderedDict([
        (
            component.alias,
            get_settings(
                component=component,
                environment=environment
            )
        )
        for component in Component.objects.all()
    ])
    if flatten:
        return flatten_dict(data)
    return data


def update_settings(component: Component, environment: Environment, settings: dict):
    """
    Update component settings.
    """

    store.update(
        component=component.alias,
        environment=environment.alias,
        settings=settings
    )

    # Notify about update component
    config_updated.send(
        sender=Component,
        component=component,
        environment=environment
    )

    return component


def delete_component(component: Component):
    """
    Delete component.
    """

    with transaction.atomic():

        component.delete()

        for environment in Environment.objects.all():
            try:
                inject_dict_params(
                    data=get_settings(
                        component=component,
                        environment=environment
                    ),
                    params=get_all_settings(environment, flatten=True),
                    flatten=True,
                    raise_exception=True
                )
            except InjectKeyError as e:
                raise ComponentDeleteError(
                    'One of other components is referring '
                    'to `%(key)s` key.' % {
                        'key': e.key
                    }
                )


def _init_store():
    klass = import_string(settings.CONFIG_STORE['class'])
    options = settings.CONFIG_STORE.get('options', {})
    return klass(**options)
