from am.configfactory.models import Component


def components(request):
    return {
        'components': Component.objects.all()
    }
