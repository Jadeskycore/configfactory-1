from distutils.util import strtobool

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from configfactory.models import Component, environment_manager
from configfactory.services import get_all_settings, get_component_settings
from configfactory.utils import inject_dict_params, flatten_dict


def environments_view(request):
    data = [{
        'alias': environment.alias,
        'name': environment.name,
        'fallback': environment.fallback,
        'url': request.build_absolute_uri(
            reverse('api_components', kwargs={
                'environment': environment.alias
            })
        )
    } for environment in environment_manager.all()]
    return JsonResponse(data=data, safe=False)


def components_view(request, environment):

    environment = environment_manager.get_or_404(environment)
    flatten = _get_flatten_param(request)
    settings_dict = get_all_settings(environment, flatten=False)
    flatten_settings_dict = flatten_dict(settings_dict)

    if flatten:
        data = flatten_settings_dict
    else:
        data = settings_dict

    data = inject_dict_params(
        data=data,
        params=flatten_settings_dict,
        raise_exception=False
    )

    return JsonResponse(data, safe=False)


def component_settings_view(request, environment, alias):

    component = get_object_or_404(Component, alias=alias)
    environment = environment_manager.get_or_404(environment)
    flatten = _get_flatten_param(request)

    data = get_component_settings(
        component=component,
        environment=environment,
        flatten=flatten
    )

    return JsonResponse(data=data, safe=False)


def _get_flatten_param(request):
    return bool(strtobool(request.GET.get('flatten', 'no').lower()))
