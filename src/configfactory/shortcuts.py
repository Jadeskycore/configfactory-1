from django.conf import settings


def get_environment_alias(environment=None):
    if environment is None:
        return settings.BASE_ENVIRONMENT
    return environment


def is_base_environment(environment=None):
    if environment is None:
        return True
    return environment == settings.BASE_ENVIRONMENT
