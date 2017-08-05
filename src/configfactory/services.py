from collections import OrderedDict

from django.db import transaction

from configfactory.exceptions import ComponentDeleteError, InjectKeyError
from configfactory.models import Component, Environment, environment_manager
from configfactory.utils import (
    flatten_dict,
    inject_dict_params,
    json_loads,
    merge_dicts,
)


def get_component_settings(component, environment=None, flatten=False):
    """
    Get component settings.
    """

    settings_dict = json_loads(component.settings_json)
    base_settings_dict = settings_dict.get(
        Environment.base_alias,
        {}
    )

    if isinstance(environment, str):
        environment = environment_manager.get(environment)

    if environment.is_base:
        ret = base_settings_dict
    else:
        env_settings_dict = settings_dict.get(environment.alias)
        if env_settings_dict is None:
            if environment.fallback:
                env_settings_dict = settings_dict.get(
                    environment.fallback,
                    {}
                )
            else:
                env_settings_dict = {}
        ret = merge_dicts(
            base_settings_dict,
            env_settings_dict,
        )

    if flatten:
        ret = flatten_dict(ret)

    return ret


def update_component_settings(component, environment, data):
    """
    Update component settings.
    """
    component.set_settings(
        data=data,
        environment=environment.alias
    )
    component.save()
    return component


def delete_component(component: Component):
    """
    Delete component.
    """

    with transaction.atomic():

        component.delete()

        for environment in environment_manager.all():
            try:
                inject_dict_params(
                    data=get_component_settings(
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


def get_all_settings(environment, flatten=False):
    """
    Get all settings.
    """
    data = OrderedDict([
        (
            component.alias,
            get_component_settings(
                component=component,
                environment=environment
            )
        )
        for component in Component.objects.all()
    ])
    if flatten:
        return flatten_dict(data)
    return data
