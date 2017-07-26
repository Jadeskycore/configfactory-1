from collections import OrderedDict

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

from configfactory.models import Component, environments


def components(request, environment=None):

    flatten = _get_flatten_param(request)
    queryset = Component.objects.all()

    if environment:
        if environment in environments:
            data = OrderedDict([
                (c.alias, c.get_settings(environment, flatten=flatten)) for c in queryset
            ])
        else:
            raise Http404
    else:
        data = OrderedDict([
            (c.alias, c.get_all_settings(flatten=flatten)) for c in queryset
        ])

    return JsonResponse(data=data, safe=False)


def component_settings(request, environment, alias):

    component = get_object_or_404(Component, alias=alias)

    flatten = _get_flatten_param(request)
    data = component.get_settings(environment, flatten=flatten)

    return JsonResponse(data=data, safe=False)


def _get_flatten_param(request):
    try:
        return bool(int(request.GET.get('flatten', False)))
    except (TypeError, ValueError):
        return False
