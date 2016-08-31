import logging

import requests
from requests.auth import HTTPBasicAuth

from am.configfactory import settings
from am.configfactory.utils import merge_dicts
from am.configfactory.client.exceptions import ConfigFactoryClientException

logger = logging.getLogger(__name__)


class ConfigFactoryClient:

    def __init__(self, base_url: str, username: str, password: str,
                 raise_exceptions=True, environment='development',
                 default_settings=None, default_strict=None):

        self.base_url = base_url[:-1] if base_url.endswith('/') else base_url
        self.auth = HTTPBasicAuth(username, password)
        self.raise_exceptions = raise_exceptions
        self._environment = environment

        if default_settings is None:
            default_settings = {}

        self._settings = {}

        if environment in settings.ENVIRONMENTS:
            try:
                self._settings = self.load()
            except Exception as e:
                logger.warning("Cannot load settings. Using defaults. [{}]".format(str(e)))
        else:
            logger.warning("`{}` is not supported environment. Available environments are: {}.".format(
                environment,
                ', '.join(settings.ENVIRONMENTS)
            ))

        # Load default settings
        self._settings = merge_dicts(default_settings, self._settings)

        if default_strict is None:
            default_strict = False
        self._default_strict = default_strict

    def _create_url(self, path, **params):
        """
        Make url.

        :param path: Base path
        :param params: Parameters
        :return: Url
        """
        return '{base_url}{path}'.format(base_url=self.base_url, path=path.format(**params))

    def _make_request(self, method, url, params=None, timeout=None):
        """
        Make request.

        :param method: Method
        :param url: Url
        :param params: Parameters
        :param timeout: Wait timeout
        :return: Response json
        """

        if params is None:
            params = {}

        response = requests.request(method, url, auth=self.auth, params=params, timeout=timeout)
        logger.info('{} {} {}. Response ({}): {}'.format(method.upper(), url, params, response.status_code,
                                                         response.content))

        if response.status_code not in [200, 201] and self.raise_exceptions:
            raise ConfigFactoryClientException("Invalid response. Got [{}].".format(response.status_code))

        return response.json()

    @property
    def environment(self):
        return self._environment

    @property
    def settings(self):
        return self._settings

    def load(self, component: str=None):
        """
        Load settings

        :param component: Component alias
        :return: Settings
        """
        if component is None:
            url = self._create_url('/{environment}/', environment=self.environment)
        else:
            url = self._create_url('/{environment}/{component}/', environment=self.environment, component=component)
        return self._make_request('GET', url, params={'flatten': 1})

    def load_value(self, path, component=None):
        """
        Load settings value.

        :param path: Path
        :param component: Component alias
        :return: Value
        """
        if component is None:
            url = self._create_url('/{environment}/get/{path_}/', environment=self.environment, path_=path)
        else:
            url = self._create_url('/{environment}/{component}/get/{path_}/', environment=self.environment,
                                   component=component, path_=path)
        return self._make_request('GET', url)

    def reload(self):
        """
        Reload settings.
        """
        self._settings = self.load()

    def get(self, path: str, default=None, component=None, load=False, strict=None):
        """
        Get value by path.

        :param path: Path
        :param default: Default value
        :param component: Component alias
        :param load: Load directly from API
        :param strict: Strict mode
        :return: Value
        """

        if load:
            return self.load_value(path, component=component)

        if component:
            path = '.'.join([component, path])

        if strict is None:
            strict = self._default_strict

        if strict:
            return self.settings[path]
        else:
            return self.settings.get(path, default)

    def __getitem__(self, item):
        return self.get(item, strict=True)
