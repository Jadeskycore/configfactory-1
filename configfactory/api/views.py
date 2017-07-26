from collections import OrderedDict

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from configfactory.models import Component, environments


def components_view(request, environment=None):

    flatten = _get_flatten_param(request)
    components = Component.objects.all()

    if environment:
        environment = environments.get_or_404(environment)
        data = OrderedDict([
            (
                component.alias,
                component.get_settings(environment.alias, flatten=flatten)
            )
            for component in components
        ])
    else:
        data = OrderedDict([
            (
                component.alias,
                component.get_all_settings(flatten=flatten)
            )
            for component in components
        ])

    return JsonResponse(data=data, safe=False)


def component_settings_view(request, environment, alias):

    component = get_object_or_404(Component, alias=alias)
    environment = environments.get_or_404(environment)

    flatten = _get_flatten_param(request)
    data = component.get_settings(environment, flatten=flatten)

    return JsonResponse(data=data, safe=False)


def _get_flatten_param(request):
    try:
        return bool(int(request.GET.get('flatten', False)))
    except (TypeError, ValueError):
        return False
