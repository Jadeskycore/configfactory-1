from configfactory.models import Component


def update_settings(component, environment, data):
    """
    Update component settings.
    """
    component.set_settings(
        data=data,
        environment=environment.alias
    )
    component.save()
    return component


def delete_component(component):
    """
    Delete component.
    """
    component.delete()


def get_inject_params(environment):
    """
    Get global inject parameters.
    """
    return {
        {
            component.alias: component.get_settings(
                environment=environment,
                flatten=True
            )
        }
        for component in Component.objects.all()
    }
