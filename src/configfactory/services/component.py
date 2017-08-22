from django.db import transaction

from configfactory.exceptions import ComponentDeleteError, InjectKeyError
from configfactory.models import Component, Environment
from configfactory.utils import inject_dict_params


def delete_component(component: Component):
    """
    Delete component.
    """

    from .config import get_settings, get_all_settings

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
