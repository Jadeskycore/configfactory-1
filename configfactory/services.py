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
