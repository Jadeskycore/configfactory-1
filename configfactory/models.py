import collections

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.http import Http404
from django.utils.functional import cached_property

from configfactory.utils import (
    flatten_dict,
    json_dumps,
    json_loads,
    merge_dicts,
)


class Component(models.Model):

    name = models.CharField(max_length=64, unique=True)

    alias = models.SlugField(
        unique=True,
        help_text='Unique component alias'
    )

    settings_json = models.TextField(
        blank=True,
        null=True,
        default='{}'
    )

    schema_json = models.TextField(
        blank=True,
        null=True,
        default='{}'
    )

    require_schema = models.BooleanField(
        default=True,
        help_text='Use json schema validation'
    )

    is_global = models.BooleanField(
        default=False,
        help_text="Use only base environment"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    @cached_property
    def settings(self):
        return json_loads(self.settings_json)

    def get_settings(self, environment=None, flatten=False):

        settings_dict = json_loads(self.settings_json)
        base_settings_dict = settings_dict.get(
            Environment.base_alias,
            {}
        )

        if isinstance(environment, str):
            environment = environment_manager.get(environment)

        if environment.is_base:
            ret = base_settings_dict
        else:
            env_settings_dict = settings_dict.get(environment.alias)
            if env_settings_dict is None:
                if environment.fallback:
                    env_settings_dict = settings_dict.get(
                        environment.fallback,
                        {}
                    )
                else:
                    env_settings_dict = {}
            ret = merge_dicts(
                base_settings_dict,
                env_settings_dict,
            )

        if flatten:
            ret = flatten_dict(ret)

        return ret

    def set_settings(self, data, environment=None):

        if environment is None:
            environment = Environment.base_alias

        settings_dict = json_loads(self.settings_json)

        if isinstance(data, str):
            data = json_loads(data)

        settings_dict[environment] = data

        self.settings_json = json_dumps(settings_dict)

    @property
    def schema(self):
        return json_loads(self.schema_json)

    @schema.setter
    def schema(self, value):
        self.schema_json = json_dumps(value)


class Environment:

    base_alias = 'base'

    def __init__(self, alias, name=None, fallback=None):
        if name is None:
            name = alias.title()
        self.alias = alias
        self.name = name
        self.fallback = fallback

    @property
    def is_base(self):
        return self.alias == self.base_alias

    def __str__(self):
        return self.alias


class EnvironmentHandler:

    def __init__(self):
        self._environments = collections.OrderedDict([
            (
                Environment.base_alias,
                Environment(
                    alias=Environment.base_alias,
                    name='Base'
                )
            )
        ])
        for environment in getattr(settings, 'ENVIRONMENTS', []):
            alias = environment['alias']
            name = environment.get('name')
            fallback = environment.get('fallback')
            self._environments[alias] = Environment(
                alias=alias,
                name=name,
                fallback=fallback
            )

    def all(self, user: 'User' = None):
        """
        Get environment list.
        """
        if user and not user.is_admin:
            return [
                environment
                for environment in self._environments.values()
                if (
                    environment.alias in user.environments
                    or environment.is_base
                )
            ]
        return list(self._environments.values())

    def get(self, alias=None, user: 'User' = None):
        if alias is None:
            alias = Environment.base_alias
        if user and not user.is_admin:
            environments = {
                environment.alias: environment
                for environment in self.all(user)
            }
        else:
            environments = self._environments
        return environments[alias]

    def get_or_404(self, alias=None, user: 'User' = None):
        try:
            return self.get(
                alias=alias,
                user=user
            )
        except KeyError:
            raise Http404

    def __getitem__(self, item):
        return self.get(item)


class User:

    def __init__(self,
                 username,
                 password=None,
                 is_active=True,
                 is_admin=False,
                 environments=None):
        self.username = username
        self.password_hash = None
        self.is_active = is_active
        self.is_admin = is_admin
        if environments is None:
            environments = []
        self.environments = environments
        if password:
            self.set_password(password)

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password_hash)


class UserManager:

    def __init__(self):
        self._users = {}
        for user_data in getattr(settings, 'USERS', []):
            username = user_data['username']
            password = user_data.get('password')
            is_active = user_data.get('is_active', True)
            is_admin = user_data.get('is_admin', False)
            environments = user_data.get('environments')
            user = User(
                username=username,
                password=password,
                is_active=is_active,
                is_admin=is_admin,
                environments=environments
            )
            self._users[username] = user

    def get(self, username):
        try:
            return self._users[username]
        except KeyError:
            return None


user_manager = UserManager()
environment_manager = EnvironmentHandler()
