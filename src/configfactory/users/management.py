from django.apps import apps as global_apps
from django.contrib.auth import get_user_model
from django.db import DEFAULT_DB_ALIAS, router

from configfactory.users import settings


def create_default_users(app_config,
                         verbosity=2,
                         using=DEFAULT_DB_ALIAS,
                         apps=global_apps,
                         **kwargs):
    try:
        User = get_user_model()
    except LookupError:
        return

    if not router.allow_migrate_model(using, User):
        return
