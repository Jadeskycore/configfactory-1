import configfactory
from configfactory.models import Component


def version(request):
    return {
        'version': configfactory.__version__
    }


def auth(request):
    return {
        'current_user':  request.user
    }


def components(request):
    return {
        'components': Component.objects.all(),
    }
