import configfactory
from configfactory.models import Component


def version(request):
    return {
        'version': configfactory.__version__
    }


def components(request):
    return {
        'components': Component.objects.all()
    }
