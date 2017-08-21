from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):

    name = 'configfactory.users'
    verbose_name = _("Users")
