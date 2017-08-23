from distutils.util import strtobool

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from configfactory.models import Component, Environment
from configfactory.services import config


def environments_view(request):
    data = [{
        'alias': environment.alias,
        'name': environment.name,
        'fallback': environment.fallback.alias if environment.fallback_id else None,
        'url': request.build_absolute_uri(
            reverse('api_components', kwargs={
                'environment': environment.alias
            })
        )
    } for environment in Environment.objects.active()]
    return JsonResponse(data=data, safe=False)


def components_view(request, environment):

    environment = get_object_or_404(Environment, alias=environment)
    flatten = _get_flatten_param(request)

    data = config.inject_settings_params(
        environment=environment,
        data=config.get_all_settings(environment, flatten=flatten),
        raise_exception=False
    )

    return JsonResponse(data, safe=False)


def component_settings_view(request, environment, alias):

    component = get_object_or_404(Component, alias=alias)
    environment = get_object_or_404(Environment, alias=environment)
    flatten = _get_flatten_param(request)

    data = config.get_settings(
        environment=environment,
        component=component,
        flatten=flatten
    )

    return JsonResponse(data=data, safe=False)


def _get_flatten_param(request):
    return bool(strtobool(request.GET.get('flatten', 'no').lower()))
