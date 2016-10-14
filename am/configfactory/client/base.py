import os
import json
import logging
import requests
from requests.auth import HTTPBasicAuth

from am.configfactory.utils import merge_dicts
from am.configfactory.client.exceptions import ConfigFactoryError

logger = logging.getLogger(__name__)


class ConfigFactory:

    def __init__(self,
                 base_url: str,
                 username: str,
                 password: str,
                 environment='development',
                 default_settings=None,
                 default_strict=None,
                 use_cache=False,
                 cache_root=None,
                 cache_filename='configfactory.json',
                 ):

        self._base_url = base_url[:-1] \
            if base_url.endswith('/') else base_url
        self._auth = HTTPBasicAuth(username, password)
        self._environment = environment

        default_settings = default_settings or {}
        settings = {}

        if default_strict is None:
            default_strict = False
        self._default_strict = default_strict

        if cache_root is None:
            cache_root = '/var/tmp'

        self._use_cache = use_cache
        self._cache_filename = os.path.join(cache_root, cache_filename)

        try:
            settings = self.load()
        except Exception as e:
            logger.warning(
                "Cannot load remote settings: {} "
                "Using defaults.".format(str(e)))

        # Load default settings
        self._settings = merge_dicts(default_settings, settings)

    @property
    def environment(self):
        return self._environment

    @property
    def settings(self):
        return self._settings

    def _create_url(self, path, **params) -> str:
        """
        Make url.

        :param path: Base path
        :param params: Parameters
        :return: Url
        """
        return '{base_url}{path}'.format(
            base_url=self._base_url,
            path=path.format(**params)
        )

    def _make_request(self, url, params=None):
        """
        Make request.

        :param url: Url
        :param params: Parameters
        :return: Response json
        """

        params = params or {}

        logger.info("GET {} [SENDING]: {}.".format(url, params))

        try:
            response = requests.request(
                method='GET',
                url=url,
                auth=self._auth,
                params=params,
            )
        except requests.RequestException as e:
            message = "ConfigFactory request error: {}.".format(e)
            logger.error(message)
            raise ConfigFactoryError(message)

        logger.info('GET {} [RESPONSE({})].'.format(url, params, response.status_code))

        # Check for success status
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            message = "ConfigFactory response error: {}.".format(e)
            logger.error(message)
            raise ConfigFactoryError(message)

        try:
            return response.json()
        except (TypeError, ValueError) as e:
            message = "ConfigFactory parse error: {}.".format(e)
            logger.error(message)
            return ConfigFactoryError(message)

    def load(self, component: str=None, use_cache=None):
        """
        Load settings.

        :param component: Component alias
        :param use_cache: Use cache
        :return: Settings
        """

        settings = None

        if use_cache is None:
            use_cache = self._use_cache

        if use_cache:
            settings = self._read_cache()

        if settings is None:

            if component is None:
                url = self._create_url(
                    path='/{environment}/',
                    environment=self.environment
                )
            else:
                url = self._create_url(
                    path='/{environment}/{component}/',
                    environment=self.environment,
                    component=component
                )

            settings = self._make_request(url, params={'flatten': 1})

            if use_cache:
                self._write_cache(settings)

        return settings or {}

    def _read_cache(self) -> dict:
        """
        Load settings from cache.

        :return: Settings
        """
        try:
            with open(self._cache_filename) as f:
                return json.load(f)
        except IOError:
            return None

    def _write_cache(self, settings):
        """
        Write settings to the cache.
        """
        with open(self._cache_filename, 'w') as f:
            json.dump(settings, f, ensure_ascii=False)

    def reload(self):
        """
        Reload settings.
        """
        self._settings = self.load()

    def get(self, path: str, default=None, component=None, strict=None):
        """
        Get value by path.

        :param path: Path
        :param default: Default value
        :param component: Component alias
        :param strict: Strict mode
        :return: Value
        """

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
