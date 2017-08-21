from django.apps import apps as global_apps
from django.db import DEFAULT_DB_ALIAS, router

from configfactory.environments import settings


def create_environments(app_config,
                        verbosity=2,
                        using=DEFAULT_DB_ALIAS,
                        apps=global_apps,
                        **kwargs):
    try:
        Environment = apps.get_model('environments', 'Environment')
    except LookupError:
        return

    if not router.allow_migrate_model(using, Environment):
        return

    environments = settings.ENVIRONMENTS
    aliases = set()

    # Create or active environments
    for order, environment_data in enumerate(environments, start=1):

        alias = environment_data['alias']  # type: str
        name = environment_data.get('name', alias.title())
        aliases.add(alias)

        try:
            environment = Environment.objects.using(using).get(alias=alias)
            if verbosity >= 2:
                print("Updating {alias} environment.".format(alias=alias))
            environment.name = name
            environment.order = order
            environment.is_active = True
            environment.save(using=using)
        except Environment.DoesNotExist:
            environment = Environment(alias=alias, name=name, order=order)
            if verbosity >= 2:
                print("Creating {alias} environment.".format(alias=alias))
            environment.save(using=using)

    # Diactivate olb environment
    for environment in Environment.objects.using(using).all():
        alias = environment.alias
        aliases.add(alias)
        if alias not in aliases and alias != settings.BASE_ENVIRONMENT:
            if verbosity >= 2:
                print("Diactivating {alias} environment.".format(alias=alias))
            environment.is_active = False
            environment.save(using=using)

    # Set environment fallback
    for environment_data in environments:
        alias = environment_data['alias']
        fallback = environment_data.get('fallback')
        try:
            environment = Environment.objects.using(using).get(alias=alias)
            fallback_environment = Environment.objects.using(using).filter(
                alias=fallback
            ).first()
            if verbosity >= 2:
                print(
                    "Setting {alias} fallback environment.".format(
                        alias=environment.alias
                    )
                )
            environment.fallback = fallback_environment
            environment.save(using=using)
        except Environment.DoesNotExist:
            continue

    # Create base environment
    if settings.BASE_ENVIRONMENT not in aliases:

        alias = settings.BASE_ENVIRONMENT
        name = alias.title()

        environment = Environment()
        environment.alias = alias
        environment.name = name
        environment.order = -1
        environment.is_active = True
        environment.save(using=using)
