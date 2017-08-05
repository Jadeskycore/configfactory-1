from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from configfactory.models import Component, environment_manager
from configfactory.services import get_all_settings
from configfactory.utils import inject_dict_params


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

    flatten = _get_flatten_param(request)
    environment = environment_manager.get_or_404(environment)

    data = inject_dict_params(
        data=get_all_settings(
            environment=environment,
            flatten=flatten
        ),
        params=get_all_settings(environment, flatten=True),
        raise_exception=False
    )

    return JsonResponse(data, safe=False)


def component_settings_view(request, environment, alias):

    component = get_object_or_404(Component, alias=alias)
    environment = environment_manager.get_or_404(environment)

    flatten = _get_flatten_param(request)
    data = component.get_settings(environment, flatten=flatten)

    return JsonResponse(data=data, safe=False)


def _get_flatten_param(request):
    try:
        return bool(int(request.GET.get('flatten', False)))
    except (TypeError, ValueError):
        return False
