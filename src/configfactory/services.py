from collections import OrderedDict

from configfactory.exceptions import ComponentDeleteError, InjectKeyError
from django.db import transaction

from configfactory.models import Component, environment_manager
from configfactory.utils import flatten_dict, inject_dict_params


def update_settings(component, environment, data):
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
                    data=component.get_settings(environment),
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
            component.get_settings(environment)
        )
        for component in Component.objects.all()
    ])
    if flatten:
        return flatten_dict(data)
    return data
