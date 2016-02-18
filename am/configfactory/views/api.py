from collections import OrderedDict

from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from am.configfactory import backup
from am.configfactory.models import Component
from am.configfactory.utils import flatten_dict, sort_dict


@require_http_methods(["POST"])
def backup_dump(request):
    name = backup.dump()
    return JsonResponse(data=name, safe=False)


@require_http_methods(["POST"])
def backup_cleanup(request):
    backup.cleanup()
    return JsonResponse(data=True, safe=False)


def components(request, environment=None, path=None):

    flatten = _get_flatten_param(request)
    queryset = Component.objects.all()

    if environment:
        if environment in settings.ENVIRONMENTS:
            data = OrderedDict([
                (c.alias, c.get_settings(environment)) for c in queryset
            ])
        else:
            raise Http404
    else:
        data = OrderedDict([
            (c.alias, c.get_all_settings()) for c in queryset
        ])

    if path:
        data = flatten_dict(data)
        data = data.get(path)

    if flatten:
        data = sort_dict(flatten_dict(data))

    return JsonResponse(data=data, safe=False)


def component_settings(request, environment, alias, path=None):

    component = get_object_or_404(Component, alias=alias)

    flatten = _get_flatten_param(request) or path is not None
    data = component.get_settings(environment)

    if path:
        data = data.get(path)

    if flatten:
        data = sort_dict(flatten_dict(data))

    return JsonResponse(data=data, safe=False)


def _get_flatten_param(request):
    try:
        return bool(int(request.GET.get('flatten', False)))
    except TypeError:
        return False
