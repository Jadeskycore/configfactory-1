from collections import OrderedDict

from django.conf import settings
from django.db import transaction
from django.utils.functional import SimpleLazyObject
from django.utils.module_loading import import_string

from configfactory.exceptions import ComponentDeleteError, InjectKeyError
from configfactory.models import Component, Environment
from configfactory.shortcuts import get_environment_alias
from configfactory.signals import component_deleted, config_updated
from configfactory.stores.base import ConfigStore
from configfactory.utils import flatten_dict, inject_dict_params, merge_dicts

store = SimpleLazyObject(func=lambda: _init_store())  # type: ConfigStore


def get_settings(environment: Environment, component: Component, flatten=False):
    """
    Get component settings.
    """

    if environment.is_base:
        data = store.get(environment.alias, component.alias)
    else:
        base_settings = store.get(get_environment_alias(), component.alias)
        env_settings = store.get(environment.alias, component.alias)
        if env_settings is None:
            if environment.fallback_id:
                fallback = environment.fallback.alias
                env_settings = store.get(fallback, component.alias)
            else:
                env_settings = {}

        data = merge_dicts(base_settings, env_settings)

    if flatten:
        data = flatten_dict(data)

    return data


def get_all_settings(environment: Environment, flatten=False):
    """
    Get all settings.
    """

    components = Component.objects.all()

    data = OrderedDict([
        (
            component.alias,
            get_settings(environment, component)
        )
        for component in components
    ])

    if flatten:
        return flatten_dict(data)

    return data


def inject_settings_params(environment, data, components=None, raise_exception=True):

    def _getter(components=None):

        if components is None:
            components = Component.objects.all()

        return flatten_dict(OrderedDict([
            (
                component.alias,
                get_settings(environment, component)
            )
            for component in components
        ]))

    params = SimpleLazyObject(func=lambda: _getter(components))  # type: dict

    return inject_dict_params(
        data=data,
        params=params,
        raise_exception=raise_exception
    )


def update_settings(component: Component, environment: Environment, settings: dict):
    """
    Update component settings.
    """

    store.update(
        environment=environment.alias,
        component=component.alias,
        settings=settings
    )

    # Notify about updated component
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
            data = get_settings(environment, component)
            try:
                inject_settings_params(
                    environment=environment,
                    data=data,
                    raise_exception=True
                )
            except InjectKeyError as e:
                raise ComponentDeleteError(
                    'One of other components is referring '
                    'to `%(key)s` key.' % {
                        'key': e.key
                    }
                )

        # Notify about deleted component
        component_deleted.send(sender=Component, component=component)


def _init_store():
    klass = import_string(settings.CONFIG_STORE['class'])
    options = settings.CONFIG_STORE.get('options', {})
    return klass(**options)
